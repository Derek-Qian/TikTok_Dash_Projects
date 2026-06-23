from __future__ import annotations

import asyncio
import logging
from typing import Any

import feffery_antd_components as fac
from dash import Input, Output, State, callback, no_update

from src.database.engine import create_session
from src.database.repository import get_all_products, get_tiktok_credentials
from src.services.push_service import PushService
from src.web.callbacks.table_callbacks import _make_row

logger = logging.getLogger(__name__)


@callback(
    [
        Output("data-table", "data", allow_duplicate=True),
        Output("btn-push-batch", "loading"),
        Output("global-message", "children", allow_duplicate=True),
    ],
    Input("btn-push-batch", "nClicks"),
    State("data-table", "selectedRows"),
    prevent_initial_call=True,
)
def handle_push_batch(
    n_clicks: int | None,
    selected_rows: list[dict[str, object]] | None,
) -> tuple[object, bool, object]:
    if not n_clicks or not selected_rows:
        return no_update, False, fac.AntdMessage(type="warning", content="请先选择商品")

    product_ids = [str(r["product_id"]) for r in selected_rows]

    async def _run() -> tuple[list[dict[str, Any]], dict[str, Any]]:
        async with create_session() as session:
            creds = await get_tiktok_credentials(session, region="MY")
            if not creds:
                raise RuntimeError("未找到马来西亚 TikTok 认证信息，请检查 tk_shops 和 tk_auth_info 表")
            service = PushService(
                app_key=creds["app_key"],
                app_secret=creds["app_secret"],
                access_token=creds["access_token"],
                shop_cipher=creds["shop_cipher"],
                region=creds.get("region", ""),
            )
            success_count = 0
            failed_count = 0
            fail_details: list[str] = []
            results = await service.push_batch(product_ids)
            for r in results:
                if r.success:
                    success_count += 1
                else:
                    failed_count += 1
                    fail_details.append(f"{r.product_id}: {r.error}")
            rows = await get_all_products(session)
        return rows, {
            "success": success_count,
            "failed": failed_count,
            "fail_details": fail_details,
        }

    try:
        rows, stats = asyncio.run(_run())
        success: Any = stats["success"]
        failed: Any = stats["failed"]
        fail_details: Any = stats["fail_details"]
        content = f"推送完成：成功 {success}，失败 {failed}"
        if fail_details:
            content += f"（{'; '.join(fail_details[:3])}）"
        msg_type = "success" if failed == 0 else "warning" if success else "error"
        data_list = [_make_row(r) for r in rows]
        return data_list, False, fac.AntdMessage(type=msg_type, content=content)
    except Exception as e:
        logger.exception("批量推送失败: %s", e)
        return no_update, False, fac.AntdMessage(type="error", content=f"批量推送失败: {e}")
