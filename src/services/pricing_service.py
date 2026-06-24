from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RegionPricing:
    """区域定价配置"""

    currency: str
    exchange_rate: float  # 1 CNY = ? 目标货币
    margin_rate: float  # 利润率，例如 0.5 表示 50%
    platform_fee_rate: float = 0.0  # 平台费率，例如 0.05 表示 5%
    min_price: float = 0.0
    round_to: float = 0.01  # 保留两位小数


# 简化的区域默认定价配置（CNY → 目标货币）
_REGION_PRICING_MAP: dict[str, RegionPricing] = {
    "MY": RegionPricing(currency="MYR", exchange_rate=0.62, margin_rate=0.6, platform_fee_rate=0.05, min_price=1.0),
    "VN": RegionPricing(currency="VND", exchange_rate=3500, margin_rate=0.55, platform_fee_rate=0.05, min_price=10000),
    "TH": RegionPricing(currency="THB", exchange_rate=4.8, margin_rate=0.6, platform_fee_rate=0.05, min_price=30),
    "PH": RegionPricing(currency="PHP", exchange_rate=7.8, margin_rate=0.6, platform_fee_rate=0.05, min_price=50),
    "ID": RegionPricing(currency="IDR", exchange_rate=2200, margin_rate=0.6, platform_fee_rate=0.05, min_price=10000),
    "SG": RegionPricing(currency="SGD", exchange_rate=0.19, margin_rate=0.5, platform_fee_rate=0.05, min_price=1.0),
    "US": RegionPricing(currency="USD", exchange_rate=0.14, margin_rate=0.5, platform_fee_rate=0.08, min_price=1.0),
    "GB": RegionPricing(currency="GBP", exchange_rate=0.11, margin_rate=0.5, platform_fee_rate=0.08, min_price=1.0),
}


def get_region_pricing(region: str) -> RegionPricing:
    """获取区域默认定价配置"""
    return _REGION_PRICING_MAP.get(region.upper(), _REGION_PRICING_MAP["US"])


def extract_original_price(raw: dict[str, Any]) -> float | None:
    """从 1688 原始数据中提取原价（人民币）"""
    # 优先取批发价/单价
    for key in ("price", "salePrice", "wholesalePrice", "unitPrice"):
        value = raw.get(key)
        if value is not None:
            price = _parse_price_value(value)
            if price is not None:
                return price

    # 其次从 SKU 中找最低价格
    sku_details = raw.get("skuDetails") or {}
    if isinstance(sku_details, dict):
        variants = sku_details.get("variants") or []
        prices = [_parse_price_value(v.get("price")) for v in variants if isinstance(v, dict)]
        valid_prices = [p for p in prices if p is not None]
        if valid_prices:
            return min(valid_prices)

    # 兜底：skuList
    sku_list = raw.get("skuList") or []
    if isinstance(sku_list, list):
        prices = [_parse_price_value(v.get("price")) for v in sku_list if isinstance(v, dict)]
        valid_prices = [p for p in prices if p is not None]
        if valid_prices:
            return min(valid_prices)

    return None


def calculate_suggested_price(original_cny: float, region: str) -> float:
    """根据原价和目标市场计算建议售价"""
    cfg = get_region_pricing(region)
    # 换算 + 利润 + 平台费兜底
    local_price = original_cny * cfg.exchange_rate
    cost_with_fee = local_price * (1 + cfg.platform_fee_rate)
    final_price = cost_with_fee * (1 + cfg.margin_rate)
    final_price = max(final_price, cfg.min_price)
    return round(final_price / cfg.round_to) * cfg.round_to


def _parse_price_value(value: Any) -> float | None:
    """解析价格字段"""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value) if float(value) > 0 else None
    if isinstance(value, dict):
        for key in ("price", "amount", "current", "salePrice", "min"):
            v = value.get(key)
            if isinstance(v, (int, float)):
                return float(v) if float(v) > 0 else None
            if isinstance(v, str):
                try:
                    return float(v) if float(v) > 0 else None
                except ValueError:
                    continue
    if isinstance(value, str):
        try:
            return float(value) if float(value) > 0 else None
        except ValueError:
            return None
    return None
