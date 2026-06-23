from __future__ import annotations

import logging
import sys

import dash

from src.web.layout import render_layout

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    title="TikTok 1688 同步管理",
)

app.layout = render_layout

import src.web.callbacks.detail_callbacks  # noqa: F401, E402
import src.web.callbacks.push_callbacks  # noqa: F401, E402
import src.web.callbacks.sync_callbacks  # noqa: F401, E402
import src.web.callbacks.table_callbacks  # noqa: F401, E402

server = app.server

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
