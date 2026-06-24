from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ApifySyncParams:
    """Apify 采集参数"""

    offer_ids: list[str] | None = None
    keywords: list[str] | None = None
    max_results: int = 20
    sort_by: str = "relevance"
    merchant_type: str = "any"
    include_sku_details: bool = True
    include_description_html: bool = False
    include_supplier_intelligence: bool = False
    proxy_country_mode: str = "CN"

    def to_run_input(self) -> dict[str, Any]:
        """转换为 Apify Actor 输入"""
        return {
            "offerIds": self.offer_ids or [],
            "keywords": self.keywords or [],
            "maxResults": self.max_results,
            "sortBy": self.sort_by,
            "merchantType": self.merchant_type,
            "includeSkuDetails": self.include_sku_details,
            "includeDescriptionHtml": self.include_description_html,
            "includeSupplierIntelligence": self.include_supplier_intelligence,
            "proxyCountryMode": self.proxy_country_mode,
        }


class ApifySkuVariant:
    """SKU 变体，从原始 dict 提取"""

    def __init__(self, raw: dict[str, Any]) -> None:
        self.sku_id: str = str(raw.get("skuId", ""))
        self.specs: list[dict[str, Any]] = raw.get("specs") or []
        self.price: str | None = str(raw.get("price")) if raw.get("price") else None
        self._raw: dict[str, Any] = raw


class ApifyProduct:
    """采集到的 1688 商品"""

    def __init__(self, raw: dict[str, Any]) -> None:
        self.offer_id: str = str(raw.get("offerId", ""))
        self.title: str | None = raw.get("title")
        self._raw: dict[str, Any] = raw
        self.sku_variants: list[ApifySkuVariant] = self._parse_skus(raw)

    @staticmethod
    def _parse_skus(raw: dict[str, Any]) -> list[ApifySkuVariant]:
        sku_details = raw.get("skuDetails") or {}
        if not isinstance(sku_details, dict):
            return []
        variants_raw = sku_details.get("variants") or []
        return [ApifySkuVariant(v) for v in variants_raw]

    @property
    def base_data_json(self) -> str:
        import json
        return json.dumps(self._raw, ensure_ascii=False)
