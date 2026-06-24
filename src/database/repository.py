from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


def _now() -> datetime:
    return datetime.now()


async def upsert_batch(
    session: AsyncSession,
    batch_id: str,
    task_name: str,
) -> None:
    """幂等写入批次记录"""
    await session.execute(
        text("""
            INSERT INTO tk_fill_batches (batch_id, task_name, created_at)
            VALUES (:batch_id, :task_name, :created_at)
            ON CONFLICT (batch_id) DO NOTHING
        """),
        {"batch_id": batch_id, "task_name": task_name, "created_at": _now()},
    )
    await session.commit()


async def upsert_product(
    session: AsyncSession,
    product_id: str,
    batch_id: str,
    product_title: str | None,
    base_data: str,
    original_price: float | None = None,
    suggested_price: float | None = None,
    target_region: str | None = None,
) -> None:
    """幂等写入商品主表"""
    now = _now()
    await session.execute(
        text("""
            INSERT INTO tk_fill_products
                (product_id, batch_id, product_title, base_data,
                 category_id, brand_id, status, last_sync_error,
                 tiktok_product_id, original_price, suggested_price, target_region,
                 created_at, update_time)
            VALUES
                (:product_id, :batch_id, :product_title, :base_data,
                 NULL, NULL, 'fetched', NULL,
                 NULL, :original_price, :suggested_price, :target_region,
                 :created_at, :update_time)
            ON CONFLICT (product_id) DO UPDATE SET
                batch_id = EXCLUDED.batch_id,
                product_title = EXCLUDED.product_title,
                base_data = EXCLUDED.base_data,
                original_price = EXCLUDED.original_price,
                suggested_price = EXCLUDED.suggested_price,
                target_region = EXCLUDED.target_region,
                status = EXCLUDED.status,
                update_time = EXCLUDED.update_time
        """),
        {
            "product_id": product_id,
            "batch_id": batch_id,
            "product_title": product_title,
            "base_data": base_data,
            "original_price": original_price,
            "suggested_price": suggested_price,
            "target_region": target_region,
            "created_at": now,
            "update_time": now,
        },
    )


async def upsert_sku(
    session: AsyncSession,
    sku_id: str,
    batch_id: str,
    product_id: str,
    sku_attributes: str | None,
    price: float | None,
    sku_data: str,
) -> None:
    """幂等写入 SKU 详情"""
    now = _now()
    await session.execute(
        text("""
            INSERT INTO tk_fill_product_skus
                (sku_id, batch_id, product_id, sku_attributes, price,
                 sku_data, created_at, update_time)
            VALUES
                (:sku_id, :batch_id, :product_id, :sku_attributes, :price,
                 :sku_data, :created_at, :update_time)
            ON CONFLICT (sku_id) DO UPDATE SET
                batch_id = EXCLUDED.batch_id,
                price = EXCLUDED.price,
                sku_data = EXCLUDED.sku_data,
                update_time = EXCLUDED.update_time
        """),
        {
            "sku_id": sku_id,
            "batch_id": batch_id,
            "product_id": product_id,
            "sku_attributes": sku_attributes,
            "price": price,
            "sku_data": sku_data,
            "created_at": now,
            "update_time": now,
        },
    )


async def update_product_status(
    session: AsyncSession,
    product_id: str,
    status: str,
    error: str | None = None,
    tiktok_product_id: str | None = None,
) -> None:
    """更新商品推送状态"""
    await session.execute(
        text("""
            UPDATE tk_fill_products
            SET status = :status,
                last_sync_error = :error,
                tiktok_product_id = :tiktok_product_id,
                update_time = :update_time
            WHERE product_id = :product_id
        """),
        {
            "product_id": product_id,
            "status": status,
            "error": error,
            "tiktok_product_id": tiktok_product_id,
            "update_time": _now(),
        },
    )
    await session.commit()


async def get_all_products(session: AsyncSession) -> list[dict[str, object]]:
    """获取所有商品（供表格展示）"""
    result = await session.execute(
        text("""
            SELECT product_id, batch_id, product_title, status,
                   tiktok_product_id, original_price, suggested_price,
                   target_region, created_at
            FROM tk_fill_products
            ORDER BY created_at DESC
        """),
    )
    rows = result.fetchall()
    return [
        {
            "product_id": r[0],
            "batch_id": r[1],
            "product_title": r[2],
            "status": r[3],
            "tiktok_product_id": r[4],
            "original_price": float(r[5]) if r[5] else None,
            "suggested_price": float(r[6]) if r[6] else None,
            "target_region": r[7],
            "created_at": str(r[8]) if r[8] else None,
        }
        for r in rows
    ]


async def get_product_base_data(
    session: AsyncSession,
    product_id: str,
) -> str | None:
    """获取商品原始数据"""
    result = await session.execute(
        text("SELECT base_data FROM tk_fill_products WHERE product_id = :pid"),
        {"pid": product_id},
    )
    row = result.fetchone()
    if row and row[0]:
        return json.dumps(row[0], ensure_ascii=False) if isinstance(row[0], dict) else str(row[0])
    return None


async def get_product_skus(
    session: AsyncSession,
    product_id: str,
) -> list[dict[str, object]]:
    """获取商品的 SKU 列表"""
    result = await session.execute(
        text("""
            SELECT sku_id, sku_attributes, price, warehouse_quantity,
                   seller_sku, parcel_weight, parcel_length, parcel_width,
                   parcel_height, sku_image_uri, created_at
            FROM tk_fill_product_skus
            WHERE product_id = :pid
            ORDER BY created_at
        """),
        {"pid": product_id},
    )
    return [
        {
            "sku_id": r[0],
            "sku_attributes": r[1],
            "price": float(r[2]) if r[2] else None,
            "warehouse_quantity": r[3],
            "seller_sku": r[4],
            "parcel_weight": float(r[5]) if r[5] else None,
            "parcel_length": float(r[6]) if r[6] else None,
            "parcel_width": float(r[7]) if r[7] else None,
            "parcel_height": float(r[8]) if r[8] else None,
            "sku_image_uri": r[9],
            "created_at": str(r[10]) if r[10] else None,
        }
        for r in result.fetchall()
    ]


async def get_product_detail(
    session: AsyncSession,
    product_id: str,
) -> dict[str, object] | None:
    """获取单个商品的详细信息"""
    result = await session.execute(
        text("""
            SELECT product_id, product_title, status, batch_id,
                   category_id, brand_id, tiktok_product_id,
                   original_price, suggested_price, target_region,
                   created_at, update_time
            FROM tk_fill_products
            WHERE product_id = :pid
        """),
        {"pid": product_id},
    )
    row = result.fetchone()
    if not row:
        return None
    return {
        "product_id": row[0],
        "product_title": row[1],
        "status": row[2],
        "batch_id": row[3],
        "category_id": row[4],
        "brand_id": row[5],
        "tiktok_product_id": row[6],
        "original_price": float(row[7]) if row[7] else None,
        "suggested_price": float(row[8]) if row[8] else None,
        "target_region": row[9],
        "created_at": str(row[10]) if row[10] else None,
        "update_time": str(row[11]) if row[11] else None,
    }


async def mark_products_reviewed(
    session: AsyncSession,
    product_ids: list[str],
) -> int:
    """将商品标记为已检查（可推送）"""
    if not product_ids:
        return 0
    result = await session.execute(
        text("""
            UPDATE tk_fill_products
            SET status = 'reviewed',
                update_time = :update_time
            WHERE product_id = ANY(:ids)
              AND status IN ('fetched', 'failed')
        """),
        {
            "ids": product_ids,
            "update_time": _now(),
        },
    )
    await session.commit()
    return int(result.rowcount)


async def update_suggested_price(
    session: AsyncSession,
    product_id: str,
    suggested_price: float,
) -> None:
    """更新商品建议价格"""
    await session.execute(
        text("""
            UPDATE tk_fill_products
            SET suggested_price = :suggested_price,
                update_time = :update_time
            WHERE product_id = :product_id
        """),
        {
            "product_id": product_id,
            "suggested_price": suggested_price,
            "update_time": _now(),
        },
    )
    await session.commit()


async def get_tiktok_credentials(
    session: AsyncSession,
    region: str | None = None,
) -> dict[str, str] | None:
    if region:
        sql = """
            SELECT s.shop_cipher, a.app_key, a.app_secret, a.access_token, s.region, s.shop_id
            FROM tk_shops s
            JOIN tk_auth_info a ON s.app_key = a.app_key
            WHERE s.region = :region
            LIMIT 1
        """
        params = {"region": region.upper()}
    else:
        sql = """
            SELECT s.shop_cipher, a.app_key, a.app_secret, a.access_token, s.region, s.shop_id
            FROM tk_shops s
            JOIN tk_auth_info a ON s.app_key = a.app_key
            LIMIT 1
        """
        params = {}
    result = await session.execute(text(sql), params)
    row = result.fetchone()
    if not row:
        return None
    return {
        "shop_cipher": str(row[0]) if row[0] else "",
        "app_key": str(row[1]) if row[1] else "",
        "app_secret": str(row[2]) if row[2] else "",
        "access_token": str(row[3]) if row[3] else "",
        "region": str(row[4]) if row[4] else "",
        "shop_id": str(row[5]) if row[5] else "",
    }


async def upsert_warehouses(
    session: AsyncSession,
    warehouses: list[dict[str, Any]],
) -> None:
    import json as _json

    now = _now()
    valid_ids: set[str] = set()
    for w in warehouses:
        wid = str(w.get("id", ""))
        if not wid:
            continue
        valid_ids.add(wid)
        address_data = _json.dumps(w.get("address", {}), ensure_ascii=False)
        await session.execute(
            text("""
                INSERT INTO tk_warehouses (warehouse_id, name, effect_status, type, sub_type,
                    is_default, entity_id, address_data, created_at)
                VALUES (:wid, :name, :status, :type, :sub_type, :is_default, :entity_id,
                    :address_data, :now)
                ON CONFLICT (warehouse_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    effect_status = EXCLUDED.effect_status,
                    type = EXCLUDED.type,
                    sub_type = EXCLUDED.sub_type,
                    is_default = EXCLUDED.is_default,
                    entity_id = EXCLUDED.entity_id,
                    address_data = EXCLUDED.address_data
            """),
            {
                "wid": wid,
                "name": str(w.get("name", "")),
                "status": str(w.get("effect_status", "")),
                "type": str(w.get("type", "")),
                "sub_type": str(w.get("sub_type", "")),
                "is_default": bool(w.get("is_default")),
                "entity_id": str(w.get("entity_id", "")),
                "address_data": address_data,
                "now": now,
            },
        )
    # 清理已失效的仓库记录，避免默认仓库落到不存在的旧 ID
    if valid_ids:
        await session.execute(
            text("DELETE FROM tk_warehouses WHERE warehouse_id <> ALL(:ids)"),
            {"ids": list(valid_ids)},
        )
    await session.commit()


async def get_default_warehouse_id(session: AsyncSession) -> str | None:
    # 优先使用默认的销售仓库
    result = await session.execute(
        text("""
            SELECT warehouse_id FROM tk_warehouses
            WHERE is_default = TRUE AND effect_status = 'ENABLED'
            ORDER BY type = 'SALES_WAREHOUSE' DESC
            LIMIT 1
        """),
    )
    row = result.fetchone()
    if row:
        return str(row[0])
    # 其次选择任意销售仓库
    result = await session.execute(
        text("""
            SELECT warehouse_id FROM tk_warehouses
            WHERE effect_status = 'ENABLED' AND type = 'SALES_WAREHOUSE'
            LIMIT 1
        """),
    )
    row = result.fetchone()
    if row:
        return str(row[0])
    # 最后兜底：任意可用仓库
    result = await session.execute(
        text("SELECT warehouse_id FROM tk_warehouses WHERE effect_status = 'ENABLED' LIMIT 1"),
    )
    row = result.fetchone()
    return str(row[0]) if row else None
