from __future__ import annotations

from src.apify.schemas import ApifyProduct


def test_apify_product_parse() -> None:
    """测试 ApifyProduct 能正确解析原始 dict"""
    raw = {
        "offerId": 123456789,
        "title": "测试商品 A",
        "skuDetails": {
            "variants": [
                {"skuId": "s001", "specs": [{"name": "颜色", "value": "红"}], "price": "99.00"},
                {"skuId": "s002", "specs": [{"name": "颜色", "value": "蓝"}], "price": "109.00"},
            ],
        },
    }
    product = ApifyProduct(raw)
    assert product.offer_id == "123456789"
    assert product.title == "测试商品 A"
    assert len(product.sku_variants) == 2
    assert product.sku_variants[0].sku_id == "s001"
    assert product.sku_variants[0].price == "99.00"
    assert product.sku_variants[1].sku_id == "s002"


def test_apify_product_no_sku() -> None:
    """测试没有 SKU 时也能正常解析"""
    raw = {"offerId": "999", "title": "无 SKU 商品"}
    product = ApifyProduct(raw)
    assert product.offer_id == "999"
    assert len(product.sku_variants) == 0
