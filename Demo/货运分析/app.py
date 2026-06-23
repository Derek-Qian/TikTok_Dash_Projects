# 导入需要的包
import uuid
import time
import dash
import json
import pandas as pd
from dash import html,set_props
import feffery_antd_components as fac
import feffery_utils_components as fuc
import feffery_leaflet_components as flc
from feffery_dash_utils.style_utils import style
from dash.dependencies import Input,Output,State
from get_data import get_data_list

# 获取数据
regions,freight_plans = get_data_list()

# 创建看板
app = dash.Dash(
    __name__,
    update_title=None, # 刷新浏览器是不显示updating
    title="货运分析地图", # 浏览器标签页标题
    suppress_callback_exceptions=True, # 允许预加载未完成时回调
)

app.layout = html.Div(
    [
        fuc.FefferyTopProgress(
            html.Div(
                [
                    # logo标题区块 & 筛选区块
                    fac.AntdRow(
                        fac.AntdCol(
                            html.Div(
                                [
                                    # 全局消息提示
                                    fac.Fragment(id="global-message"),
                                    # logo & 标题 & 标题说明
                                    fac.AntdSpace(
                                        [
                                            # logo & 标题
                                            fac.AntdSpace(
                                                [
                                                    # 标题logo
                                                    html.Img(src="/assets/imgs/logo.svg", height=64),
                                                    # 标题
                                                    fac.AntdText(
                                                        "货运分析地图",
                                                        style=style(fontSize=30),
                                                    ),
                                                ]
                                            ),
                                            # 标题说明
                                            fac.AntdText(
                                                "针对全国不同区域间的货运情况进行可视化展示，建议不要选择过多的地区，以便更好地展示结果",
                                                type="secondary",
                                            ),
                                            
                                        ],
                                        direction="vertical", # 垂直布局
                                        size=0,
                                        
                                    ),
                                    fac.AntdDivider(), # 分割线
                                    # 筛选区块
                                    fac.AntdRow(
                                        [
                                            fac.AntdCol(
                                                # 构建表单项
                                                fac.AntdFormItem(
                                                    # 下拉选项
                                                    fac.AntdSelect(
                                                        id="departure-regions",
                                                        placeholder="请选择",
                                                        options=freight_plans["出发地区"].unique().tolist(),
                                                        mode="multiple",
                                                        maxTagCount="responsive",
                                                    ),
                                                    label="出发地",
                                                    layout="horizontal", # horizontal水平；vertical垂直
                                                    style=style(margin=0)
                                                ),
                                                span=12
                                            ),
                                            fac.AntdCol(
                                                # 构建表单项
                                                fac.AntdFormItem(
                                                    # 下拉选项
                                                    fac.AntdSelect(
                                                        id="destination-regions",
                                                        placeholder="请选择",
                                                        options=freight_plans["到达地区"].unique().tolist(),
                                                        mode="multiple",
                                                        maxTagCount="responsive",
                                                    ),
                                                    label="目的地",
                                                    layout="horizontal", # horizontal水平；vertical垂直
                                                    style=style(margin=0)
                                                ),
                                                span=12
                                            ),
                                            fac.AntdCol(
                                                fac.AntdButton(
                                                    "查询分析",
                                                    id="submit-button",
                                                    type="primary",
                                                    block=True,
                                                    loadingChildren="分析中",
                                                ),
                                                span=24
                                            ),
                                        ],
                                        gutter=[25,15]
                                    ),
                                ], 
                                className="my-card"
                            ),
                            span=24,
                        ),                     
                        style={"height": "30%", "marginBottom": "15px"}
                    ),

                    # 展示区块
                    fac.AntdRow(
                        [
                            # 整体分为两列，左右比3:1
                            fac.AntdCol(
                                html.Div(
                                    [
                                        flc.LeafletMap(
                                            [flc.LeafletTileLayer()],
                                            center={
                                                "lat": 35.134386211514155,
                                                "lng": 106.91839944442702,
                                            },
                                            zoom=4,
                                            viewAutoCorrection=True,
                                            style=style(height="100%"),
                                        ),
                                    ],
                                    id="map-container",
                                    className="my-card", # 容器样式设置
                                ),
                                span=18,
                            ),
                            fac.AntdCol(
                                html.Div(
                                    [],
                                    id="table-container",
                                    className="my-card"
                                ),
                                span=6
                            ),
                            
                        ],
                        gutter=15, # 间距为15
                        style={"height": "calc(70% - 15px)"}
                    ),
                ],
                style={"height":"100%"}
            ),
            style={"height":"100%"},
            listenPropsMode="include",
            includeProps=["map-container.children","table-container.children"],
            minimum=0.4,
        )
    ],
    className="main-container" # 样式设置，上下左右边距配置等；
)

@app.callback(
    output=dict(
        map_container=Output("map-container","children"),
        table_container=Output("table-container","children"),
    ),
    inputs=dict(
        nClicks=Input("submit-button","nClicks")
    ),
    state=dict(
        departure_regions=State("departure-regions", "value"),
        destination_regions=State("destination-regions","value")
    ),
    running=[(Output("submit-button", "loading"), True, False)],
    prevent_initial_call=True,       
)
def update_result(nClicks,departure_regions, destination_regions):
    if not (departure_regions and destination_regions):
        # 给出系统提示
        set_props(
            "global-message",
            {"children": fac.AntdMessage(content="请先完善查询条件", type="warning")},
        )
        return dict(
            map_container=dash.no_update,
            table_container=dash.no_update
        )
    
    else:
        time.sleep(0.5)

        # 提取目标货运记录数据
        match_freight_plans = (

            freight_plans.query(
                "出发地区 in @departure_regions and 到达地区 in @destination_regions")
                .groupby(['出发地区','到达地区'],as_index=False)
                .agg(
                    {
                        "出发地区经度": "first",
                        "出发地区纬度": "first",
                        "到达地区经度": "first",
                        "到达地区纬度": "first",
                        "出发时间": "count",
                    }
                )
                .rename(columns={"出发时间":"货运班次"})
                .sort_values("货运班次",ascending=False)
        )

        # 聚合统计
        flowData = [
            {
                "from": {
                    "lng": flow["出发地区经度"],
                    "lat": flow["出发地区纬度"],
                },
                "to": {
                    "lng": flow["到达地区经度"],
                    "lat": flow["到达地区纬度"],
                },
                "labels": {
                    "from": flow["出发地区"],
                    "to": flow["到达地区"],
                },
                "value": flow["货运班次"],
            }
            for flow in match_freight_plans.to_dict("records")
        ]

        # 刷新地图
        map_container = fac.AntdRow(
            [
                fac.AntdCol(
                    flc.LeafletMap(
                        [
                            flc.LeafletTileLayer(),
                            # 流线图层
                            flc.LeafletFlowLayer(
                                flowData=flowData,
                                arcLabelFontSize="16px",
                                keepUniqueLabels=True,
                            ),
                            # 相关区域矢量图层
                            flc.LeafletGeoJSON(
                                data={
                                    **regions,
                                    "features":[
                                        region
                                        for region in regions["features"]
                                        if region["properties"]["name"]
                                        in departure_regions
                                        or region["properties"]["name"]
                                        in destination_regions
                                    ],
                                },
                                defaultStyle={"fillOpacity": 0.1, "weight": 2}
                            ),
                        ],
                        key=str(uuid.uuid4()),
                        viewAutoCorrection=True,
                        style={"height":"100%"}
                    ),
                    flex="auto"
                )
            ],
            wrap=False,
            style={"height":"100%"}
        )

        # 刷新table
        table_container = fac.AntdRow(
            [
                fac.AntdCol(
                    html.Div(
                        fac.AntdTable(
                            data=match_freight_plans[
                                    ["出发地区", "到达地区", "货运班次"]
                                ].to_dict("records"),
                            columns=[
                                {
                                    "dataIndex": "出发地区",
                                    "title": "出发地区",
                                },
                                {
                                    "dataIndex": "到达地区",
                                    "title": "到达地区",
                                },
                                {
                                    "dataIndex": "货运班次",
                                    "title": "货运班次",
                                },
                            ],
                            tableLayout="fixed",
                            size="small",
                            pagination=False,
                            sortOptions={"sortDataIndexes": ["货运班次"]},
                            summaryRowContents=(
                                # 仅在多地区时渲染总结栏
                                [
                                    {
                                        "content": fac.AntdText(
                                            "总计班次：{}".format(
                                                match_freight_plans["货运班次"].sum()
                                            ),
                                            strong=True,
                                        ),
                                        "colSpan": 3,
                                        "align": "center",
                                    },
                                ]
                                if match_freight_plans.shape[0] > 1 else []
                            )
                            
                        ),
                        style=style(height="100%", overflowY="auto")
                    ), 
                    flex="auto"
                ),
            ],
            style={"height":"100%"}
        ),

        return dict(
            map_container=map_container,
            table_container=table_container
        )

if __name__ == '__main__':
    app.run(port=8089,debug=True)