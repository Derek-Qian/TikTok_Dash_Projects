from __future__ import annotations

import feffery_antd_components as fac
import feffery_utils_components as fuc

from src.web.components.data_table import render_data_table
from src.web.components.sync_controls import render_sync_controls


def render_layout() -> fac.AntdRow:
    return fac.AntdRow(
        [
            fac.AntdCol(
                [
                    fac.AntdTitle("TikTok 1688 商品同步管理", level=3),
                    render_sync_controls(),
                    fac.AntdDivider(),
                    fac.AntdSpin(
                        render_data_table(),
                        id="sync-spinner",
                        indicator=fuc.FefferyExtraSpinner(type="push"),
                        delay=300,
                    ),
                    fuc.FefferyTimeout(id="table-init-trigger", delay=100),
                    fac.AntdCenter(id="global-message"),
                    fac.AntdModal(
                        fac.Fragment(id="product-detail-content"),
                        id="product-detail-modal",
                        visible=False,
                        width=900,
                        renderFooter=False,
                    ),
                ],
                span=22,
                offset=1,
            ),
        ],
    )
