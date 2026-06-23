from __future__ import annotations

import asyncio
import logging
import time
import traceback

from dash import Input, Output, callback

from src.database.engine import create_session
from src.database.repository import get_all_products

logger = logging.getLogger(__name__)


def _link_1688(product_id: str) -> str:
    return f"https://detail.1688.com/offer/{product_id}.html"


_STATUS_MAP: dict[str, str] = {
    "pending": "待推送",
    "pushing": "推送中",
    "pushed": "已推送",
    "failed": "推送失败",
}


def _make_row(r: dict[str, object]) -> dict[str, object]:
    pid = str(r["product_id"])
    raw_status = str(r.get("status") or "pending")
    return {
        "product_id": pid,
        "product_title": r["product_title"],
        "status": _STATUS_MAP.get(raw_status, raw_status),
        "batch_id": r["batch_id"],
        "link_1688": _link_1688(pid),
        "created_at": str(r["created_at"]) if r.get("created_at") else None,
    }


@callback(
    Output("data-table", "data", allow_duplicate=True),
    Input("table-init-trigger", "timeoutCount"),
    prevent_initial_call=True,
)
def load_table_data(n_clicks: int | None) -> list[dict[str, object]]:
    async def _fetch() -> list[dict[str, object]]:
        async with create_session() as session:
            return await get_all_products(session)

    last_err: str = ""
    for attempt in range(1, 4):
        try:
            rows = asyncio.run(_fetch())
            return [_make_row(r) for r in rows]
        except Exception:
            last_err = traceback.format_exc()
            logger.warning("加载表格数据失败 (attempt %d/3)", attempt)
            time.sleep(attempt)
    print(f"[table_callbacks] 3次重试均失败:\n{last_err}", flush=True)
    return []
