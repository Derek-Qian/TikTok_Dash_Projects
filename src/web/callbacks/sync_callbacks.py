from __future__ import annotations

import asyncio
import logging
from typing import Any

import feffery_antd_components as fac
from dash import Input, Output, State, callback, no_update

from src.apify.schemas import ApifySyncParams
from src.database.engine import create_session
from src.database.repository import get_all_products
from src.services.sync_service import SyncService
from src.web.callbacks.table_callbacks import _make_row

logger = logging.getLogger(__name__)


@callback(
    [
        Output("data-table", "data", allow_duplicate=True),
        Output("btn-sync", "loading"),
        Output("global-message", "children", allow_duplicate=True),
    ],
    Input("btn-sync", "nClicks"),
    [
        State("sync-keywords", "value"),
        State("sync-offer-ids", "value"),
        State("sync-max-results", "value"),
        State("sync-sort-by", "value"),
        State("sync-merchant-type", "value"),
        State("sync-target-region", "value"),
        State("sync-include-sku", "checked"),
        State("sync-include-desc", "checked"),
        State("sync-include-supplier", "checked"),
        State("data-table", "data"),
    ],
    prevent_initial_call=True,
)
def handle_sync(
    n_clicks: int | None,
    keywords: str | None,
    offer_ids: str | None,
    max_results: int | None,
    sort_by: str | None,
    merchant_type: str | None,
    target_region: str | None,
    include_sku: bool,
    include_desc: bool,
    include_supplier: bool,
    current_data: list[dict[str, object]],
) -> tuple[object, bool, object]:
    if not n_clicks:
        return no_update, False, no_update

    keyword_list = _split_text(keywords)
    offer_id_list = _split_text(offer_ids)

    if not keyword_list and not offer_id_list:
        return no_update, False, fac.AntdMessage(
            type="warning",
            content="请至少输入关键词或商品 ID",
        )

    params = ApifySyncParams(
        keywords=keyword_list,
        offer_ids=offer_id_list,
        max_results=max(1, min(max_results or 20, 1000)),
        sort_by=sort_by or "relevance",
        merchant_type=merchant_type or "any",
        include_sku_details=bool(include_sku),
        include_description_html=bool(include_desc),
        include_supplier_intelligence=bool(include_supplier),
    )

    async def _run() -> tuple[dict[str, object], list[dict[str, object]]]:
        service = SyncService()
        async with create_session() as session:
            result = await service.run(
                session,
                params=params,
                target_region=target_region or "MY",
            )
            rows = await get_all_products(session)
        return result, rows

    try:
        result, rows = asyncio.run(_run())
        logger.info("Sync done: %s", result)
        if result.get("error"):
            return no_update, False, fac.AntdMessage(type="error", content=str(result["error"]))
        data_list = [_make_row(r) for r in rows]
        msg = f"采集完成：成功 {result['success']} 条，失败 {result['failed']} 条，SKU {result['sku_count']} 个"
        return data_list, False, fac.AntdMessage(type="success", content=msg)
    except Exception as e:
        logger.exception("Sync failed: %s", e)
        return no_update, False, fac.AntdMessage(type="error", content=f"采集失败: {e}")


@callback(
    [
        Output("sync-keywords", "value"),
        Output("sync-offer-ids", "value"),
        Output("sync-max-results", "value"),
        Output("sync-sort-by", "value"),
        Output("sync-merchant-type", "value"),
        Output("sync-target-region", "value"),
        Output("sync-include-sku", "checked"),
        Output("sync-include-desc", "checked"),
        Output("sync-include-supplier", "checked"),
        Output("global-message", "children", allow_duplicate=True),
    ],
    Input("btn-sync-reset", "nClicks"),
    prevent_initial_call=True,
)
def reset_sync_form(n_clicks: int | None) -> tuple[Any, ...]:
    if not n_clicks:
        return [no_update] * 9 + [no_update]
    return (
        None,
        None,
        20,
        "relevance",
        "any",
        "MY",
        True,
        False,
        False,
        fac.AntdMessage(type="success", content="已重置采集参数"),
    )


@callback(
    Output("sync-spinner", "spinning"),
    Input("btn-sync", "loading"),
    Input("btn-push-batch", "loading"),
)
def toggle_spinner(sync_loading: bool, push_loading: bool) -> bool:
    return sync_loading or push_loading


def _split_text(value: str | None) -> list[str]:
    if not value:
        return []
    return [v.strip() for v in str(value).split(",") if v.strip()]
