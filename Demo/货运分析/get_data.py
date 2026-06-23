import json
import pandas as pd

def get_data_list():
    # 读取地图文件
    with open(r"./中华人民共和国.json",encoding="utf-8") as fp:
        regions = json.load(fp) # 将json文件加载转换为python对象；dump操作则相反；
    
    # 读取物流数据
    freight_plans = pd.read_csv(r"./示例数据.csv")

    return regions,freight_plans