from __future__ import annotations

import asyncio
import logging

import feffery_antd_components as fac
from dash import Input, Output, State, callback, no_update

from src.database.engine import create_session
from src.database.repository import get_product_detail, get_product_skus

logger = logging.getLogger(__name__)


@callback(
    [
        Output("product-detail-modal", "visible"),
        Output("product-detail-modal", "title"),
        Output("product-detail-content", "children"),
    ],
    Input("data-table", "nClicksCell"),
    State("data-table", "recentlyCellClickRecord"),
    State("data-table", "recentlyCellClickColumn"),
    prevent_initial_call=True,
)
def show_product_detail(
    n_clicks: int | None,
    record: dict[str, object] | None,
    column: str | None,
) -> tuple[bool, str, object]:
    if not n_clicks or not record:
        return False, "", no_update

    if column != "product_title":
        return False, "", no_update

    product_id = str(record["product_id"])

    async def _fetch() -> tuple[dict[str, object] | None, list[dict[str, object]]]:
        async with create_session() as session:
            detail = await get_product_detail(session, product_id)
            skus = await get_product_skus(session, product_id)
        return detail, skus

    try:
        detail, skus = asyncio.run(_fetch())

        if not detail:
            return False, "", no_update

        info_items = [
            {"label": "商品 ID", "children": detail.get("product_id", "")},
            {"label": "商品标题", "children": detail.get("product_title", "")},
            {"label": "状态", "children": detail.get("status", "")},
            {"label": "批次号", "children": detail.get("batch_id", "")},
            {"label": "TikTok ID", "children": detail.get("tiktok_product_id") or "-"},
            {"label": "创建时间", "children": detail.get("created_at") or "-"},
            {"label": "更新时间", "children": detail.get("update_time") or "-"},
            {"label": "类目", "children": detail.get("category_id") or "-"},
            {"label": "品牌", "children": detail.get("brand_id") or "-"},
        ]

        sku_columns = [
            {"title": "SKU ID", "dataIndex": "sku_id", "width": 120},
            {"title": "规格属性", "dataIndex": "sku_attributes", "width": 180},
            {"title": "价格", "dataIndex": "price", "width": 70},
            {"title": "库存", "dataIndex": "warehouse_quantity", "width": 60},
            {"title": "商家SKU", "dataIndex": "seller_sku", "width": 110},
            {"title": "重量(g)", "dataIndex": "parcel_weight", "width": 70},
            {"title": "长×宽×高(cm)", "dataIndex": "parcel_length", "width": 130},
        ]

        sku_data = [
            {
                "sku_id": s.get("sku_id"),
                "sku_attributes": s.get("sku_attributes"),
                "price": s.get("price"),
                "warehouse_quantity": s.get("warehouse_quantity"),
                "seller_sku": s.get("seller_sku"),
                "parcel_weight": s.get("parcel_weight"),
                "parcel_length": (
                    f"{s.get('parcel_length')}×{s.get('parcel_width')}×{s.get('parcel_height')}"
                    if s.get("parcel_length")
                    else "-"
                ),
            }
            for s in skus
        ]

        content = fac.AntdSpace(
            [
                fac.AntdDescriptions(
                    items=info_items,
                    bordered=True,
                    size="small",
                    column=2,
                ),
                fac.AntdDivider(f"SKU 明细（共 {len(skus)} 个）"),
                fac.AntdTable(
                    columns=sku_columns,
                    data=sku_data,
                    bordered=True,
                    size="small",
                ),
            ],
            direction="vertical",
            style={"width": "100%"},
        )
        title = str(record.get("product_title", product_id))
        return True, title, content

    except Exception:
        logger.exception("获取商品详情失败")
        return False, "", no_update
