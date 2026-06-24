from __future__ import annotations

import json
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.apify import ApifyService
from src.apify.schemas import ApifyProduct, ApifySyncParams
from src.database.repository import upsert_batch, upsert_product, upsert_sku
from src.services.pricing_service import calculate_suggested_price, extract_original_price

logger = logging.getLogger(__name__)


class SyncService:
    """数据同步服务：采集 -> 清洗 -> 写入"""

    def __init__(self) -> None:
        self._apify = ApifyService()

    async def run(
        self,
        session: AsyncSession,
        params: ApifySyncParams | None = None,
        target_region: str = "MY",
    ) -> dict[str, object]:
        params = params or ApifySyncParams(offer_ids=[])
        result = self._apify.sync(params)
        if not result.batch_id:
            return {"error": "未指定商品 ID 或关键词，跳过采集"}

        task_name = self._build_task_name(result)
        await upsert_batch(session, result.batch_id, task_name)
        logger.info("批次记录已创建: %s", result.batch_id)

        success = 0
        failed_ids: list[str] = []
        sku_total = 0

        for product in result.products:
            try:
                await self._write_product(session, product, result.batch_id, target_region)
                sku_total += len(product.sku_variants)
                success += 1
                logger.info("商品 %s 同步成功 (SKU: %d)", product.offer_id, len(product.sku_variants))
            except Exception:
                await session.rollback()
                logger.exception("商品 %s 同步失败", product.offer_id)
                failed_ids.append(product.offer_id)

        if failed_ids:
            await session.commit()

        return {
            "batch_id": result.batch_id,
            "total": result.total,
            "success": success,
            "failed": len(failed_ids),
            "sku_count": sku_total,
            "failed_ids": failed_ids,
        }

    @staticmethod
    def _build_task_name(result: object) -> str:
        params = getattr(result, "params", None)
        keywords = getattr(params, "keywords", None) or []
        offer_ids = getattr(params, "offer_ids", None) or []
        parts: list[str] = []
        if keywords:
            parts.append(f"关键词-{','.join(keywords)}")
        if offer_ids:
            parts.append(f"offer-{len(offer_ids)}")
        return f"1688-sync-{result.total}-items-{'-'.join(parts) or 'default'}"

    @staticmethod
    async def _write_product(
        session: AsyncSession,
        product: ApifyProduct,
        batch_id: str,
        target_region: str,
    ) -> None:
        raw = product._raw
        original_price = extract_original_price(raw)
        suggested_price = (
            calculate_suggested_price(original_price, target_region)
            if original_price is not None
            else None
        )

        await upsert_product(
            session,
            product_id=product.offer_id,
            batch_id=batch_id,
            product_title=product.title,
            base_data=product.base_data_json,
            original_price=original_price,
            suggested_price=suggested_price,
            target_region=target_region,
        )

        for sku in product.sku_variants:
            if not sku.sku_id or sku.sku_id == "None":
                continue
            price_val: float | None = None
            if sku.price:
                try:
                    price_val = float(sku.price)
                except ValueError:
                    price_val = None
            await upsert_sku(
                session,
                sku_id=sku.sku_id,
                batch_id=batch_id,
                product_id=product.offer_id,
                sku_attributes=json.dumps(sku.specs, ensure_ascii=False),
                price=price_val,
                sku_data=json.dumps(sku._raw, ensure_ascii=False),
            )

        await session.commit()
