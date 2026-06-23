from __future__ import annotations

import feffery_antd_components as fac


def render_sync_controls() -> fac.AntdRow:
    """同步操作按钮区"""
    return fac.AntdRow(
        [
            fac.AntdButton(
                "开始同步",
                id="btn-sync",
                type="primary",
                icon=fac.AntdIcon(icon="antd-sync"),
                style={"marginRight": 8},
            ),
            fac.AntdButton(
                "批量推送",
                id="btn-push-batch",
                type="primary",
                danger=True,
                icon=fac.AntdIcon(icon="antd-cloud-upload"),
            ),
        ],
        style={"marginBottom": 16},
    )
