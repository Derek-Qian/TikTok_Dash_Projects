from __future__ import annotations

import feffery_antd_components as fac

_TITLE_FMT = (  # noqa: E501
    "(value) => React.createElement('span', "
    "{style: {color:'#1677ff', textDecoration:'underline', cursor:'pointer'}}, value)"
)

_LINK_FMT = (  # noqa: E501
    "(value) => value ? React.createElement('a', "
    "{href: value, target: '_blank', style: {color:'#1677ff', cursor:'pointer'}}, '查看') : ''"
)


def render_data_table() -> fac.AntdTable:
    return fac.AntdTable(
        id="data-table",
        columns=[
            {"title": "商品 ID", "dataIndex": "product_id", "width": 140, "editable": False},
            {
                "title": "商品标题",
                "dataIndex": "product_title",
                "width": 280,
                "editable": False,
                "renderOptions": {"renderType": "custom-format"},
            },
            {"title": "状态", "dataIndex": "status", "width": 90, "editable": False},
            {"title": "批次号", "dataIndex": "batch_id", "width": 170, "editable": False},
            {
                "title": "1688链接",
                "dataIndex": "link_1688",
                "width": 100,
                "editable": False,
                "renderOptions": {"renderType": "custom-format"},
            },
            {"title": "创建时间", "dataIndex": "created_at", "width": 150, "editable": False},
        ],
        customFormatFuncs={
            "product_title": _TITLE_FMT,
            "link_1688": _LINK_FMT,
        },
        enableCellClickListenColumns=["product_title"],
        rowSelectionType="checkbox",
        rowSelectionWidth=50,
        bordered=True,
        size="small",
        pagination={
            "pageSize": 20,
            "showSizeChanger": True,
            "pageSizeOptions": [10, 20, 50, 100],
            "showQuickJumper": True,
        },
        style={"width": "100%"},
    )
