from __future__ import annotations

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


def transform_1688_to_tiktok(
    raw_1688_json: str,
    warehouse_id: str = "",
    locale: str = "en-US",
    currency: str = "USD",
    auto_translate: bool = False,
    main_image_uris: list[str] | None = None,
    category_id_override: str | None = None,
) -> dict[str, Any]:
    raw = json.loads(raw_1688_json)

    title = str(raw.get("title") or _find_title(raw) or "")
    description = str(raw.get("description") or _find_description(raw) or "")
    skus = _extract_skus(raw, warehouse_id, currency)
    dims = _extract_dimensions(raw)

    category_id = category_id_override or _find_category(raw)

    payload: dict[str, Any] = {
        "save_mode": "LISTING",
        "title": title,
        "description": description,
        "external_product_id": str(raw.get("offerId", "")),
        "locale": locale,
        "auto_translate_enabled": auto_translate,
    }

    if category_id:
        payload["category_id"] = category_id

    if main_image_uris:
        payload["main_images"] = [{"uri": u} for u in main_image_uris]
    else:
        images = _extract_images(raw)
        if images:
            payload["main_images"] = images

    if dims:
        if "length" in dims:
            payload["package_dimensions"] = {
                "length": str(dims["length"]),
                "width": str(dims["width"]),
                "height": str(dims["height"]),
                "unit": "CENTIMETER",
            }
        if "weight" in dims:
            payload["package_weight"] = {
                "value": str(dims["weight"]),
                "unit": "KILOGRAM",
            }

    if skus:
        payload["skus"] = skus

    return payload


def _find_category(raw: dict[str, Any]) -> str | None:
    cat_id = raw.get("categoryId") or raw.get("topCategoryId")
    if cat_id:
        return str(cat_id)
    return None


def _find_title(raw: dict[str, Any]) -> str | None:
    for key in ("productName", "productTitle", "name"):
        if raw.get(key):
            return str(raw[key])
    return None


def _find_description(raw: dict[str, Any]) -> str | None:
    for key in ("productDescription", "detailDescription", "productDetail", "desc"):
        v = raw.get(key)
        if isinstance(v, str) and v.strip():
            return v
        if isinstance(v, dict) and v.get("text"):
            return str(v["text"])
    return None


def _extract_images(raw: dict[str, Any]) -> list[dict[str, str]]:
    imgs = raw.get("images") or raw.get("imageList") or []
    if not isinstance(imgs, list):
        return []
    result: list[dict[str, str]] = []
    for img in imgs:
        if isinstance(img, str):
            result.append({"uri": img})
        elif isinstance(img, dict):
            uri = img.get("url") or img.get("imageUrl") or img.get("large") or ""
            if uri:
                result.append({"uri": str(uri)})
    return result


def _extract_skus(raw: dict[str, Any], warehouse_id: str, currency: str) -> list[dict[str, Any]]:
    sku_details = raw.get("skuDetails") or {}
    if isinstance(sku_details, dict):
        variants_raw = sku_details.get("variants") or []
    else:
        variants_raw = []

    if not variants_raw:
        variants_raw = raw.get("skuList") or raw.get("variants") or []

    skus: list[dict[str, Any]] = []
    top_price = _parse_price(raw.get("price"))
    for v in variants_raw:
        if not isinstance(v, dict):
            continue
        sku: dict[str, Any] = {}

        sku_id = str(v.get("skuId") or v.get("id") or "")
        if sku_id:
            sku["seller_sku"] = sku_id
            sku["external_sku_id"] = sku_id

        price_val = _parse_price(v.get("price")) or top_price
        if price_val is not None:
            sku["price"] = {"amount": str(price_val), "currency": currency}

        qty = v.get("stock") or v.get("quantity") or v.get("warehouse_quantity")
        if qty is not None:
            try:
                sku["inventory"] = [{"warehouse_id": warehouse_id, "quantity": int(qty)}]
            except (ValueError, TypeError):
                pass

        specs = v.get("specs") or v.get("attributes") or v.get("sales_attributes")
        attrs = _parse_sales_attributes(specs)
        if attrs:
            sku["sales_attributes"] = attrs

        if sku:
            skus.append(sku)

    if not skus:
        single: dict[str, Any] = {}
        price_val = _parse_price(raw.get("price"))
        if price_val is not None:
            single["price"] = {"amount": str(price_val), "currency": cny_currency(raw)}
            single["seller_sku"] = str(raw.get("offerId", ""))
            single["external_sku_id"] = str(raw.get("offerId", ""))
        stock = raw.get("stock") or raw.get("quantity") or raw.get("amountOnSale")
        if stock is not None:
            try:
                single["inventory"] = [{"warehouse_id": warehouse_id, "quantity": int(stock)}]
            except (ValueError, TypeError):
                pass
        if single:
            skus.append(single)

    return skus


def _extract_dimensions(raw: dict[str, Any]) -> dict[str, float]:
    result: dict[str, float] = {}

    for key in ("packageWeight", "weight"):
        w = raw.get(key)
        if isinstance(w, (int, float)):
            result["weight"] = float(w)
            break
    if "weight" not in result:
        for key in ("grossWeight", "netWeight"):
            w = raw.get(key)
            if isinstance(w, (int, float)):
                result["weight"] = float(w)
                break

    for key in ("packageSize", "packageDimensions", "dimensions"):
        d = raw.get(key)
        if isinstance(d, dict):
            for dim in ("length", "width", "height"):
                val = d.get(dim)
                if isinstance(val, (int, float)):
                    result[dim] = float(val)
            if result:
                break

    return result


def _parse_price(price_raw: Any) -> float | None:
    if price_raw is None:
        return None
    if isinstance(price_raw, (int, float)):
        return float(price_raw) if float(price_raw) > 0 else None
    if isinstance(price_raw, dict):
        for key in ("price", "salePrice", "current", "amount", "min"):
            v = price_raw.get(key)
            if isinstance(v, (int, float)):
                return float(v) if float(v) > 0 else None
            if isinstance(v, str):
                try:
                    return float(v) if float(v) > 0 else None
                except ValueError:
                    continue
    if isinstance(price_raw, str):
        try:
            return float(price_raw) if float(price_raw) > 0 else None
        except ValueError:
            return None
    return None


def cny_currency(raw: dict[str, Any]) -> str:
    price = raw.get("price") or {}
    if isinstance(price, dict):
        c = price.get("currency")
        if isinstance(c, str):
            return c
    return "CNY"


def _parse_sales_attributes(specs: Any) -> list[dict[str, Any]] | None:
    if not specs:
        return None
    if isinstance(specs, list):
        attrs: list[dict[str, Any]] = []
        for s in specs:
            if isinstance(s, dict):
                name = s.get("name") or s.get("attributeName") or ""
                value = s.get("value") or s.get("attributeValue") or ""
                if name:
                    attrs.append({"name": str(name), "value_name": str(value)})
        return attrs if attrs else None
    if isinstance(specs, str) and specs.strip():
        return [{"name": "规格", "value_name": specs.strip()}]
    return None
