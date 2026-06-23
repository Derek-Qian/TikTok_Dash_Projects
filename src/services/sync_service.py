from __future__ import annotations

import json
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.apify import ApifyService
from src.apify.schemas import ApifyProduct
from src.database.repository import upsert_batch, upsert_product, upsert_sku

logger = logging.getLogger(__name__)


class SyncService:
    """数据同步服务：采集 -> 清洗 -> 写入"""

    def __init__(self) -> None:
        self._apify = ApifyService()

    async def run(
        self,
        session: AsyncSession,
        offer_ids: list[str] | None = None,
    ) -> dict[str, object]:
        result = self._apify.sync(offer_ids)
        if not result.batch_id:
            return {"error": "未指定商品 ID，跳过采集"}

        task_name = f"1688-daily-sync-{result.total}-items"
        await upsert_batch(session, result.batch_id, task_name)
        logger.info("批次记录已创建: %s", result.batch_id)

        success = 0
        failed_ids: list[str] = []
        sku_total = 0

        for product in result.products:
            try:
                await self._write_product(session, product, result.batch_id)
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
    async def _write_product(
        session: AsyncSession,
        product: ApifyProduct,
        batch_id: str,
    ) -> None:
        await upsert_product(
            session,
            product_id=product.offer_id,
            batch_id=batch_id,
            product_title=product.title,
            base_data=product.base_data_json,
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
