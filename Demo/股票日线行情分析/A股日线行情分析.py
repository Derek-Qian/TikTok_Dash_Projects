import dash
import pandas as pd
from dash import html
import feffery_antd_components as fac
import feffery_antd_charts as fact
from dash.dependencies import Input, Output, State

# 加载数据
raw_stock_data = pd.read_csv(
    r'./A股_股票日线行情数据_20220223_20220311.csv', 
    dtype={'股票代码': 'str'},
    parse_dates=['交易日期']
)
stock_data = raw_stock_data.copy()
stock_data['交易日期'] = stock_data['交易日期'].dt.strftime('%Y-%m-%d')
stock_data = stock_data.groupby(['TS代码', '股票代码', '股票名称', '地域', '所属行业', '上市时间']).apply(
    lambda df : (
        df.sort_values('交易日期').agg({
            '收盘价': lambda s: s.tolist(),
            '涨跌额': lambda s: s.tolist(),
            '涨跌幅': lambda s: s.tolist(),
            '成交量（手）': lambda s: s.tolist(),
            '成交额（千元）': lambda s: s.tolist()
            })
    )
).reset_index(drop=False)

stock_data['周期涨幅'] = stock_data['收盘价'].apply(lambda l: (l[-1] - l[0]) / l[0])

app = dash.Dash(__name__,update_title=None)
app.title = '分析应用'
app.layout = html.Div(
    [
        fac.AntdRow(
            [
                # 左侧区域
                fac.AntdCol(
                    html.Div(
                        [
                            fac.AntdAlert(
                                message=[
                                    '通过点击下表每行左侧单选框，选择你需要进一步分析的股票',
                                    '更多dash应用开发专业知识欢迎关注芊蛋子'
                                ],
                                showIcon=True,
                                # 配置跑马灯效果
                                messageRenderMode='loop-text'
                            ),
                            fac.AntdTable(
                                id="all-stocks-info-table",
                                # 定义展示的列
                                columns=[
                                    {'title': '股票名称','dataIndex': '股票名称','fixed': False,'width': 100},
                                    {'title': 'TS代码','dataIndex': 'TS代码','fixed': False,'width': 100},
                                    {'title': '股票代码','dataIndex': '股票代码','fixed': False,'width': 100},
                                    {'title': '地域','dataIndex': '地域','fixed': False,'width': 100},
                                    {'title': '所属行业','dataIndex': '所属行业','fixed': False,'width': 100},
                                    {'title': '上市时间','dataIndex': '上市时间','fixed': False,'width': 100},
                                    {'title': '收盘价','dataIndex': '收盘价','fixed': False,'width': 100,'renderOptions':{'renderType': 'mini-area'}},
                                    {'title': '涨跌额','dataIndex': '涨跌额','fixed': False,'width': 100,'renderOptions':{'renderType': 'mini-area'}},
                                    {'title': '涨跌幅','dataIndex': '涨跌幅','fixed': False,'width': 100,'renderOptions':{'renderType': 'mini-area'}},
                                    {'title': '成交量（手）','dataIndex': '成交量（手）','fixed': False,'width': 100,'renderOptions':{'renderType': 'mini-bar'}},
                                    {'title': '成交额（千元）','dataIndex': '成交额（千元）','fixed': False,'width': 100,'renderOptions':{'renderType': 'mini-bar'}},
                                ],
                                sortOptions={'sortDataIndexes': ['上市时间']},
                                filterOptions={
                                    # keyword是关键词搜索；空字典的时候则是下拉复选；
                                    '股票代码': {'filterMode': 'keyword'},
                                    'TS代码': {'filterMode': 'keyword'},
                                    '地域': {},
                                    '所属行业': {},
                                    '股票名称': {'filterMode': 'keyword'}
                                },
                                # radio将表格设置为单选模式
                                rowSelectionType='radio',
                                # maxWidth='100%',
                                data=stock_data.to_dict('records'),
                                # 增加纵向边框
                                bordered=True,
                                # 若在列配置中设置了趋势图（line或area），该参数控制这些“迷你图”的高度
                                miniChartHeight=25,
                                # 开启分页功能
                                pagination={
                                    'pageSize': 18,
                                    'showSizeChanger': False,
                                    'showQuickJumper': True,
                                    'showTotalPrefix': '共有股票 ',
                                    'showTotalSuffix': ' 只'
                                }
                            ),
                        ],
                        # 建议引用外部css，也可以配置style字典
                        className='my-card'
                    ),
                    # 各占据50%区域
                    span=12
                ),

                # 右侧区域
                fac.AntdCol(  
                    html.Div(
                        [
                            # 右上块：calc计算高度，减去间距一半保证视觉对齐
                            html.Div(
                                fac.AntdEmpty(description="请先在左侧表格中选择要分析的股票!"),
                                id='single-stock-describe',
                                className='my-card', 
                                style={'height': 'calc(40% - 12.5px)'}
                            ),
                            # 右下块
                            html.Div(
                                fac.AntdEmpty(description="请先在左侧表格中选择要分析的股票!"), 
                                id='single-stock-chart',
                                className='my-card', 
                                style={'height': 'calc(60% - 12.5px)'}
                            ),
                        ],
                        style={
                            'height': '100%', 
                            'display': 'flex', 
                            'flexDirection': 'column', 
                            'justifyContent': 'space-between'
                        }
                    ),
                    # 各占据50%区域
                    span=12
                ),
            ],
            # 设置列与列之间的推荐间距
            gutter=25,
            # 强制这一行占据父容器 100% 的高度
            style={'height':'100%'}
        )
    ],
    className='main-container'  
)

@app.callback(
    [Output('single-stock-describe', 'children'),
     Output('single-stock-chart', 'children')],
    Input('all-stocks-info-table', 'selectedRows')
)
def analysis_selected_stock(selectedRows):
    if selectedRows:
        selected_single_stock_info = (
            raw_stock_data
                .query('TS代码 == "{}"'.format(selectedRows[0]['TS代码']))
                .reset_index(drop=True)
        )

        # 计算周期内当前个股在所有个股中的涨幅排名
        range_gains_rank = (
            stock_data
                .assign(排名=lambda df: df['周期涨幅'].rank(ascending=False, method='first'))
                .query('TS代码 == "{}"'.format(selectedRows[0]['TS代码']))
                .iat[0, -1]
        )

        # 计算周期内当前个股在所属行业内的涨幅排名
        industry_range_gains_rank = (
            stock_data
                .query('所属行业 == "{}"'.format(selectedRows[0]['所属行业']))
                .assign(排名=lambda df: df['周期涨幅'].rank(ascending=False, method='first'))
                .query('TS代码 == "{}"'.format(selectedRows[0]['TS代码']))
                .iat[0, -1]
        )

        # 计算周期内当前个股在所属区域内的涨幅排名
        area_range_gains_rank = (
            stock_data
                .query('地域 == "{}"'.format(selectedRows[0]['地域']))
                .assign(排名=lambda df: df['周期涨幅'].rank(ascending=False, method='first'))
                .query('TS代码 == "{}"'.format(selectedRows[0]['TS代码']))
                .iat[0, -1]
        )

        # 构造右上角三个仪表盘
        antdspace = fac.AntdSpace(
            [
                # 全市场
                html.Div([
                    fac.AntdStatistic(
                        title='全市场超越',
                        value=round(100 * (1 - range_gains_rank / stock_data.shape[0]), 2),
                        precision=2,
                        suffix='%',
                        valueStyle={'color': '#1890ff'}
                    ),
                    fac.AntdProgress(
                        percent=round(100 * (1 - range_gains_rank / stock_data.shape[0]), 2),
                        type='dashboard',
                        size=85,
                        showInfo=False
                    )
                ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

                fac.AntdDivider(direction='vertical', style={'height': '100px'}),

                # 行业
                html.Div([
                    fac.AntdStatistic(
                        title='行业超越',
                        value=round(100 * (1 - industry_range_gains_rank / 
                            stock_data.query('所属行业 == "{}"'.format(selectedRows[0]['所属行业'])).shape[0]), 2),
                        precision=2,
                        suffix='%',
                        valueStyle={'color': '#52c41a'}
                    ),
                    fac.AntdProgress(
                        percent=round(100 * (1 - industry_range_gains_rank / 
                            stock_data.query('所属行业 == "{}"'.format(selectedRows[0]['所属行业'])).shape[0]), 2),
                        type='dashboard',
                        size=85,
                        showInfo=False
                    )
                ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

                fac.AntdDivider(direction='vertical', style={'height': '100px'}),

                # 地域
                html.Div([
                    fac.AntdStatistic(
                        title='地域超越',
                        value=round(100 * (1 - area_range_gains_rank / 
                            stock_data.query('地域 == "{}"'.format(selectedRows[0]['地域'])).shape[0]), 2),
                        precision=2,
                        suffix='%',
                        valueStyle={'color': '#722ed1'}
                    ),
                    fac.AntdProgress(
                        percent=round(100 * (1 - area_range_gains_rank / 
                            stock_data.query('地域 == "{}"'.format(selectedRows[0]['地域'])).shape[0]), 2),
                        type='dashboard',
                        size=85,
                        showInfo=False
                    )
                ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
            ],
            style={
                'width': '100%', 
                'height': '100%', 
                'display': 'flex', 
                'alignItems': 'center', 
                'justifyContent': 'space-around'
            }
        )

        # 构造右下角的K线图
        antdstock = fact.AntdStock(
            data = selected_single_stock_info.to_dict('records'),
            xField='交易日期',
            yAxis={
                'label':{
                    'formatter':{
                        'func':'(value) => parseFloat(value).toFixed(2)'
                    }
                }
            },
            yField=['开盘价', '收盘价', '最高价', '最低价'],
            legend={
                'itemName':{
                    'formatter':{
                        'func':'''
                        (name) => {
                            return name === 'up' ? '上涨' : '下跌'
                        }
                        '''
                    }
                }
            },
            meta={
                '交易日期': {'type': 'time'}
            },
            # 这里的 fallback 样式确保图表充满卡片
            style={'height': '100%'},
            autoFit=True
        )

        return [antdspace,antdstock]
    return dash.no_update

if __name__ == '__main__':
    app.run(port=8088,debug=True)