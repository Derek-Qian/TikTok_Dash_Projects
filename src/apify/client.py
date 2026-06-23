from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime

from apify_client import ApifyClient

from src.apify.schemas import ApifyProduct
from src.config import config

logger = logging.getLogger(__name__)


@dataclass
class SyncResult:
    """一次同步的统计结果"""
    batch_id: str
    total: int = 0
    success: int = 0
    failed: int = 0
    sku_count: int = 0
    failed_ids: list[str] = field(default_factory=list)
    products: list[ApifyProduct] = field(default_factory=list)


class ApifyService:
    """Apify 1688 采集服务封装"""

    def __init__(self) -> None:
        self._client = ApifyClient(config.APIFY_TOKEN)

    def _generate_batch_id(self) -> str:
        return f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def run_scraper(self, offer_ids: list[str]) -> str:
        """调用 Apify Actor 并返回 dataset_id"""
        run_input = {
            "offerIds": offer_ids,
            "includeSkuDetails": True,
            "proxyCountryMode": "CN",
        }
        logger.info("🚀 正在调用 Apify Actor: %s, 商品数: %d", config.APIFY_ACTOR_ID, len(offer_ids))
        run = self._client.actor(config.APIFY_ACTOR_ID).call(run_input=run_input)
        dataset_id = run.default_dataset_id  # type: ignore[union-attr]
        logger.info("📦 数据集 ID: %s", dataset_id)
        return dataset_id

    def fetch_items(self, dataset_id: str) -> list[ApifyProduct]:
        """从 dataset 拉取数据并解析为 ApifyProduct 列表"""
        dataset = self._client.dataset(dataset_id)
        items = list(dataset.iterate_items())
        logger.info("📋 获取到 %d 条原始数据", len(items))
        return [ApifyProduct(item) for item in items]

    def sync(self, offer_ids: list[str] | None = None) -> SyncResult:
        """执行一次完整采集（运行 Actor + 拉取数据），返回结构化结果"""
        offer_ids = offer_ids or config.DAILY_OFFER_IDS
        if not offer_ids:
            logger.warning("⚠️ 没有指定商品 ID，跳过采集")
            return SyncResult(batch_id="")

        batch_id = self._generate_batch_id()
        logger.info("🚀 批次 ID: %s", batch_id)

        dataset_id = self.run_scraper(offer_ids)
        products = self.fetch_items(dataset_id)

        result = SyncResult(batch_id=batch_id, products=products)
        result.total = len(products)
        return result
