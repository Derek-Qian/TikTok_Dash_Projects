from __future__ import annotations

import asyncio
import logging
import traceback
from dataclasses import dataclass

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import config
from src.database.engine import create_session
from src.database.repository import (
    get_default_warehouse_id,
    get_product_base_data,
    update_product_status,
    upsert_warehouses,
)
from src.tiktok.api import TikTokApiClient
from src.tiktok.region import get_region_info
from src.tiktok.transformer import transform_1688_to_tiktok

logger = logging.getLogger(__name__)


@dataclass
class PushResult:
    product_id: str
    success: bool
    tiktok_product_id: str | None = None
    error: str | None = None


class PushService:
    def __init__(
        self,
        app_key: str,
        app_secret: str,
        access_token: str,
        shop_cipher: str,
        region: str = "",
    ) -> None:
        self._tiktok = TikTokApiClient(
            app_key=app_key,
            app_secret=app_secret,
            access_token=access_token,
            shop_cipher=shop_cipher,
        )
        info = get_region_info(region)
        self._locale = info["locale"]
        self._currency = info["currency"]

    async def push_product(
        self,
        session: AsyncSession,
        product_id: str,
    ) -> PushResult:
        try:
            return await self._do_push(session, product_id)
        except Exception:
            logger.exception("商品 %s 推送异常", product_id)
            err_msg = f"推送异常: {traceback.format_exc()[-300:]}"
            try:
                await session.rollback()
            except Exception:
                pass
            try:
                await update_product_status(session, product_id, "failed", err_msg)
                await session.commit()
            except Exception:
                logger.exception("更新状态失败")
            return PushResult(product_id=product_id, success=False, error=err_msg[-200:])

    async def _do_push(self, session: AsyncSession, product_id: str) -> PushResult:
        base_data = await get_product_base_data(session, product_id)
        if not base_data:
            await update_product_status(session, product_id, "failed", "无原始数据")
            await session.commit()
            return PushResult(product_id=product_id, success=False, error="无原始数据")

        warehouse_id = config.TIKTOK_WAREHOUSE_ID
        if not warehouse_id:
            db_wid = await get_default_warehouse_id(session)
            if db_wid:
                warehouse_id = db_wid
            else:
                await self._sync_warehouses(session)
                db_wid = await get_default_warehouse_id(session)
                if db_wid:
                    warehouse_id = db_wid
        if not warehouse_id:
            await update_product_status(session, product_id, "failed", "缺少仓库 ID")
            await session.commit()
            return PushResult(product_id=product_id, success=False, error="缺少仓库 ID")

        image_uris = await self._upload_images(base_data)

        recommended_cat: str | None = None

        # 从商品标题/类目中猜测英文关键词，用于搜索合适的 TikTok 类目
        search_keyword = _guess_english_keyword(base_data)
        logger.info("商品 %s 搜索类目关键词: %s", product_id, search_keyword)

        if not recommended_cat:
            recommended_cat = await self._tiktok.get_v2_categories(
                keyword=search_keyword,
                locale="en-US",
            )
        if not recommended_cat:
            recommended_cat = await self._tiktok.get_v2_categories(
                keyword=search_keyword,
                locale="ms-MY",
            )
        if not recommended_cat:
            logger.warning("无法获取 V2 类目，请手动配置")

        tiktok_payload = transform_1688_to_tiktok(
            base_data,
            warehouse_id=warehouse_id,
            locale=self._locale,
            currency=self._currency,
            auto_translate=False,
            main_image_uris=image_uris if image_uris else None,
            category_id_override=recommended_cat,
        )

        import json as _json

        if not tiktok_payload.get("description"):
            tiktok_payload["description"] = f"<p>{tiktok_payload.get('title', '')}</p>"
        payload_json = _json.dumps(tiktok_payload, ensure_ascii=False)
        logger.info("推送 payload 完整: %s", payload_json)

        result = await self._tiktok.create_product(tiktok_payload)
        if result is None:
            await update_product_status(session, product_id, "failed", "API 无响应")
            await session.commit()
            return PushResult(product_id=product_id, success=False, error="API 无响应")

        if "error" in result:
            error_msg = result["error"]
            await update_product_status(session, product_id, "failed", error_msg)
            await session.commit()
            return PushResult(product_id=product_id, success=False, error=error_msg)

        tiktok_id = result.get("product_id", "")
        await update_product_status(session, product_id, "pushed", tiktok_product_id=tiktok_id)
        await session.commit()
        logger.info("商品 %s 推送成功 → TikTok ID: %s", product_id, tiktok_id)
        return PushResult(product_id=product_id, success=True, tiktok_product_id=tiktok_id)

    async def _sync_warehouses(self, session: AsyncSession) -> None:
        try:
            result = await self._tiktok.get_warehouses()
            if result and "error" not in result:
                warehouses = result.get("warehouses") or []
                if warehouses:
                    await upsert_warehouses(session, warehouses)
                    logger.info("仓库数据同步完成，共 %d 条", len(warehouses))
                    return
            logger.warning("仓库数据同步失败或无数据")
        except Exception:
            logger.exception("仓库同步异常")
            try:
                await session.rollback()
            except Exception:
                pass

    async def _upload_images(self, base_data: str) -> list[str]:
        import json as _json

        raw = _json.loads(base_data)
        img_urls = _extract_image_urls(raw)
        if not img_urls:
            return []

        uris: list[str] = []
        async with httpx.AsyncClient(timeout=30) as http:
            for url in img_urls[:9]:
                try:
                    resp = await http.get(url)
                    if resp.status_code != 200:
                        logger.warning("下载图片失败 %s: HTTP %d", url, resp.status_code)
                        continue
                    result = await self._tiktok.upload_image(resp.content, "product.jpg")
                    if result and "error" not in result:
                        uri = result.get("uri") or ""
                        if uri:
                            uris.append(uri)
                            logger.info("图片上传成功: %s", uri)
                    else:
                        logger.warning("图片上传失败 %s: %s", url, result)
                except Exception:
                    logger.exception("图片处理异常 %s", url)
        return uris

    async def push_batch(
        self,
        product_ids: list[str],
    ) -> list[PushResult]:
        # 顺序推送，避免并发导致网络拥塞和 API 限流
        results: list[PushResult] = []
        for pid in product_ids:
            async with create_session() as sess:
                result = await self.push_product(sess, pid)
                results.append(result)
        return results


def _extract_image_urls(raw: dict[str, object]) -> list[str]:
    imgs = raw.get("images") or raw.get("imageList") or []
    urls: list[str] = []
    if isinstance(imgs, list):
        for img in imgs:
            if isinstance(img, str):
                urls.append(img)
            elif isinstance(img, dict):
                u = img.get("url") or img.get("imageUrl") or img.get("large") or ""
                if u:
                    urls.append(str(u))
    return urls


def _extract_title(base_data: str) -> str:
    import json as _json

    raw = _json.loads(base_data)
    return str(raw.get("title") or raw.get("productName") or "")


def _extract_desc(base_data: str) -> str:
    import json as _json

    raw = _json.loads(base_data)
    desc = raw.get("description") or raw.get("descriptionText") or ""
    return str(desc) if desc else str(raw.get("title") or "")


def _guess_english_keyword(base_data: str) -> str:
    import json as _json

    raw = _json.loads(base_data)
    title = str(raw.get("title") or "").lower()
    category_name = str(raw.get("categoryName") or "").lower()
    combined = f"{category_name} {title}"

    keywords_map = [
        (["耳环", "耳钉", "耳饰", "earrings", "earring"], "earrings"),
        (["项链", "necklace", "链"], "necklace"),
        (["戒指", "ring"], "ring"),
        (["手链", "手镯", "bracelet", "手环"], "bracelet"),
        (["服装", "clothing", "dress", "衣服", "连衣裙", "外套"], "clothing"),
        (["鞋", "shoes", "sneaker"], "shoes"),
        (["包", "bag", "handbag", "箱包"], "bag"),
        (["手表", "watch"], "watch"),
        (["帽子", "cap", "hat"], "hat"),
    ]
    for patterns, keyword in keywords_map:
        if any(p in combined for p in patterns):
            return keyword
    return "jewelry accessories"
