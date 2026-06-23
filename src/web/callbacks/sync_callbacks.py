from __future__ import annotations

import asyncio
import logging

import feffery_antd_components as fac
from dash import Input, Output, State, callback, no_update

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
    State("data-table", "data"),
    prevent_initial_call=True,
)
def handle_sync(n_clicks: int | None, current_data: list[dict[str, object]]) -> tuple[object, bool, object]:
    if not n_clicks:
        return no_update, False, no_update

    async def _run() -> tuple[dict[str, object], list[dict[str, object]]]:
        service = SyncService()
        async with create_session() as session:
            result = await service.run(session)
            rows = await get_all_products(session)
        return result, rows

    try:
        result, rows = asyncio.run(_run())
        logger.info("Sync done: %s", result)
        data_list = [_make_row(r) for r in rows]
        msg = f"同步完成：成功 {result['success']} 条，失败 {result['failed']} 条"
        return data_list, False, fac.AntdMessage(type="success", content=msg)
    except Exception as e:
        logger.exception("Sync failed: %s", e)
        return no_update, False, fac.AntdMessage(type="error", content=f"同步失败: {e}")


@callback(
    Output("sync-spinner", "spinning"),
    Input("btn-sync", "loading"),
    Input("btn-push-batch", "loading"),
)
def toggle_spinner(sync_loading: bool, push_loading: bool) -> bool:
    return sync_loading or push_loading
