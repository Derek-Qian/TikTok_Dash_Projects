from __future__ import annotations

import feffery_antd_components as fac


# Apify 排序选项（按常见 API 输入预设）
SORT_OPTIONS = [
    {"label": "相关度", "value": "relevance"},
    {"label": "价格从低到高", "value": "priceAsc"},
    {"label": "价格从高到低", "value": "priceDesc"},
    {"label": "销量优先", "value": "salesDesc"},
    {"label": "综合评分", "value": "scoreDesc"},
]

# 商家类型选项
MERCHANT_OPTIONS = [
    {"label": "全部", "value": "any"},
    {"label": "工厂", "value": "factory"},
    {"label": "贸易公司", "value": "tradingCompany"},
    {"label": "分销商", "value": "distributor"},
]

# 目标市场选项（用于建议价计算）
REGION_OPTIONS = [
    {"label": "马来西亚", "value": "MY"},
    {"label": "越南", "value": "VN"},
    {"label": "泰国", "value": "TH"},
    {"label": "菲律宾", "value": "PH"},
    {"label": "印尼", "value": "ID"},
    {"label": "新加坡", "value": "SG"},
    {"label": "美国", "value": "US"},
    {"label": "英国", "value": "GB"},
]


def render_sync_controls() -> fac.AntdCard:
    """同步参数录入区（折叠卡片 + 表单）"""
    return fac.AntdCard(
        [
            fac.AntdForm(
                [
                    fac.AntdRow(
                        [
                            fac.AntdCol(
                                [
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id="sync-keywords",
                                            placeholder="输入关键词，多个用英文逗号分隔，例如：耳环,项链",
                                            allowClear=True,
                                        ),
                                        label="关键词",
                                        tooltip="按关键词搜索 1688 商品",
                                    ),
                                ],
                                span=12,
                            ),
                            fac.AntdCol(
                                [
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id="sync-offer-ids",
                                            placeholder="输入 offerId，多个用英文逗号分隔",
                                            allowClear=True,
                                        ),
                                        label="商品 ID",
                                        tooltip="精确指定 1688 offerId",
                                    ),
                                ],
                                span=12,
                            ),
                        ],
                        gutter=16,
                    ),
                    fac.AntdRow(
                        [
                            fac.AntdCol(
                                [
                                    fac.AntdFormItem(
                                        fac.AntdInputNumber(
                                            id="sync-max-results",
                                            min=1,
                                            max=1000,
                                            defaultValue=20,
                                            style={"width": "100%"},
                                        ),
                                        label="拉取条数",
                                    ),
                                ],
                                span=8,
                            ),
                            fac.AntdCol(
                                [
                                    fac.AntdFormItem(
                                        fac.AntdSelect(
                                            id="sync-sort-by",
                                            options=SORT_OPTIONS,
                                            defaultValue="relevance",
                                            style={"width": "100%"},
                                        ),
                                        label="排序方式",
                                    ),
                                ],
                                span=8,
                            ),
                            fac.AntdCol(
                                [
                                    fac.AntdFormItem(
                                        fac.AntdSelect(
                                            id="sync-merchant-type",
                                            options=MERCHANT_OPTIONS,
                                            defaultValue="any",
                                            style={"width": "100%"},
                                        ),
                                        label="商家类型",
                                    ),
                                ],
                                span=8,
                            ),
                        ],
                        gutter=16,
                    ),
                    fac.AntdRow(
                        [
                            fac.AntdCol(
                                [
                                    fac.AntdFormItem(
                                        fac.AntdSelect(
                                            id="sync-target-region",
                                            options=REGION_OPTIONS,
                                            defaultValue="MY",
                                            style={"width": "100%"},
                                        ),
                                        label="目标市场",
                                        tooltip="用于计算建议售价",
                                    ),
                                ],
                                span=8,
                            ),
                            fac.AntdCol(
                                [
                                    fac.AntdFormItem(
                                        fac.AntdSpace(
                                            [
                                                fac.AntdSwitch(
                                                    id="sync-include-sku",
                                                    checked=True,
                                                ),
                                                fac.AntdText("包含 SKU 详情"),
                                            ]
                                        ),
                                        label="SKU 详情",
                                    ),
                                ],
                                span=8,
                            ),
                            fac.AntdCol(
                                [
                                    fac.AntdFormItem(
                                        fac.AntdSpace(
                                            [
                                                fac.AntdSwitch(
                                                    id="sync-include-desc",
                                                    checked=False,
                                                ),
                                                fac.AntdText("包含 HTML 描述"),
                                            ]
                                        ),
                                        label="描述",
                                    ),
                                ],
                                span=8,
                            ),
                        ],
                        gutter=16,
                    ),
                    fac.AntdRow(
                        [
                            fac.AntdCol(
                                [
                                    fac.AntdFormItem(
                                        fac.AntdSpace(
                                            [
                                                fac.AntdSwitch(
                                                    id="sync-include-supplier",
                                                    checked=False,
                                                ),
                                                fac.AntdText("包含供应商情报"),
                                            ]
                                        ),
                                        label="供应商情报",
                                    ),
                                ],
                                span=12,
                            ),
                        ],
                        gutter=16,
                    ),
                    fac.AntdRow(
                        [
                            fac.AntdCol(
                                [
                                    fac.AntdSpace(
                                        [
                                            fac.AntdButton(
                                                "开始采集",
                                                id="btn-sync",
                                                type="primary",
                                                icon=fac.AntdIcon(icon="antd-sync"),
                                                autoSpin=True,
                                            ),
                                            fac.AntdButton(
                                                "重置参数",
                                                id="btn-sync-reset",
                                                icon=fac.AntdIcon(icon="antd-reload"),
                                            ),
                                        ],
                                        size="middle",
                                    ),
                                ],
                            ),
                        ],
                        style={"marginTop": 16},
                    ),
                ],
                layout="vertical",
            ),
        ],
        title="📦 1688 数据采集参数",
        variant="bordered",
        style={"marginBottom": 16},
        styles={"header": {"fontWeight": "bold"}},
    )
