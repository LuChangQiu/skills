# 地图组件静态数据美化方案

> 当用户需要为地图组件配置静态数据（无数据集）时，直接使用本文件中的数据，
> 无需重新设计，保证视觉效果丰富美观。

---

## 省份 GDP 数据（2023年实际值，亿元）

适用组件：JAreaMap、JBarMap（省级粒度）

```python
PROVINCE_GDP = [
    {"name": "广东", "value": 135673}, {"name": "江苏", "value": 122875},
    {"name": "山东", "value": 92069},  {"name": "浙江", "value": 82553},
    {"name": "河南", "value": 61345},  {"name": "四川", "value": 60132},
    {"name": "湖北", "value": 55803},  {"name": "福建", "value": 53109},
    {"name": "湖南", "value": 50012},  {"name": "安徽", "value": 46015},
    {"name": "上海", "value": 47218},  {"name": "北京", "value": 43760},
    {"name": "河北", "value": 42370},  {"name": "陕西", "value": 33786},
    {"name": "江西", "value": 32200},  {"name": "重庆", "value": 30145},
    {"name": "辽宁", "value": 28975},  {"name": "云南", "value": 28803},
    {"name": "广西", "value": 26612},  {"name": "天津", "value": 16311},
    {"name": "内蒙古", "value": 23159}, {"name": "山西", "value": 25647},
    {"name": "贵州", "value": 20164},  {"name": "新疆", "value": 19125},
    {"name": "黑龙江", "value": 15901}, {"name": "吉林", "value": 13070},
    {"name": "甘肃", "value": 10545},  {"name": "海南", "value": 7173},
    {"name": "宁夏", "value": 5315},   {"name": "青海", "value": 3799},
    {"name": "西藏", "value": 2392},
]
```

---

## 城市经纬度散点数据（24城，[经度, 纬度, 指标值]）

适用组件：JBubbleMap、JBarMap（市级坐标）、JHeatMap

```python
CITY_SCATTER = [
    {"name": "北京",   "value": [116.46, 39.92, 95]},
    {"name": "上海",   "value": [121.48, 31.22, 87]},
    {"name": "广州",   "value": [113.23, 23.16, 73]},
    {"name": "深圳",   "value": [114.07, 22.62, 68]},
    {"name": "成都",   "value": [104.06, 30.67, 62]},
    {"name": "杭州",   "value": [120.19, 30.26, 58]},
    {"name": "武汉",   "value": [114.31, 30.52, 55]},
    {"name": "西安",   "value": [108.95, 34.27, 48]},
    {"name": "南京",   "value": [118.78, 32.04, 45]},
    {"name": "重庆",   "value": [106.54, 29.59, 43]},
    {"name": "天津",   "value": [117.2,  39.13, 40]},
    {"name": "郑州",   "value": [113.65, 34.76, 38]},
    {"name": "苏州",   "value": [120.62, 31.32, 36]},
    {"name": "长沙",   "value": [113.0,  28.21, 34]},
    {"name": "沈阳",   "value": [123.38, 41.8,  30]},
    {"name": "青岛",   "value": [120.33, 36.07, 28]},
    {"name": "昆明",   "value": [102.73, 25.04, 25]},
    {"name": "大连",   "value": [121.62, 38.92, 23]},
    {"name": "厦门",   "value": [118.1,  24.46, 21]},
    {"name": "哈尔滨", "value": [126.63, 45.75, 18]},
    {"name": "宁波",   "value": [121.56, 29.86, 17]},
    {"name": "济南",   "value": [117.0,  36.65, 15]},
    {"name": "合肥",   "value": [117.27, 31.86, 14]},
    {"name": "福州",   "value": [119.3,  26.08, 13]},
]
```

---

## 飞线数据（15条城市间贸易/物流路线）

适用组件：JFlyLineMap

```python
FLY_LINE_DATA = [
    {"fromName": "北京", "toName": "上海",  "coords": [[116.46,39.92],[121.48,31.22]], "value": 520},
    {"fromName": "北京", "toName": "广州",  "coords": [[116.46,39.92],[113.23,23.16]], "value": 380},
    {"fromName": "上海", "toName": "成都",  "coords": [[121.48,31.22],[104.06,30.67]], "value": 260},
    {"fromName": "广州", "toName": "武汉",  "coords": [[113.23,23.16],[114.31,30.52]], "value": 195},
    {"fromName": "北京", "toName": "西安",  "coords": [[116.46,39.92],[108.95,34.27]], "value": 310},
    {"fromName": "上海", "toName": "杭州",  "coords": [[121.48,31.22],[120.19,30.26]], "value": 450},
    {"fromName": "成都", "toName": "重庆",  "coords": [[104.06,30.67],[106.54,29.59]], "value": 280},
    {"fromName": "广州", "toName": "深圳",  "coords": [[113.23,23.16],[114.07,22.62]], "value": 420},
    {"fromName": "北京", "toName": "沈阳",  "coords": [[116.46,39.92],[123.38,41.8]],  "value": 175},
    {"fromName": "上海", "toName": "南京",  "coords": [[121.48,31.22],[118.78,32.04]], "value": 390},
    {"fromName": "武汉", "toName": "长沙",  "coords": [[114.31,30.52],[113.0,28.21]],  "value": 215},
    {"fromName": "北京", "toName": "天津",  "coords": [[116.46,39.92],[117.2,39.13]],  "value": 600},
    {"fromName": "成都", "toName": "昆明",  "coords": [[104.06,30.67],[102.73,25.04]], "value": 165},
    {"fromName": "上海", "toName": "青岛",  "coords": [[121.48,31.22],[120.33,36.07]], "value": 285},
    {"fromName": "广州", "toName": "福州",  "coords": [[113.23,23.16],[119.3,26.08]],  "value": 235},
]
```

---

## 时间轴飞线数据（4季度×8路线 = 32条，按 type 区分）

适用组件：JTotalFlyLineMap

```python
TOTAL_FLY_DATA = []
periods = ['2023Q1', '2023Q2', '2023Q3', '2023Q4']
routes = [
    ("北京", "上海",  [116.46,39.92], [121.48,31.22]),
    ("广州", "北京",  [113.23,23.16], [116.46,39.92]),
    ("上海", "成都",  [121.48,31.22], [104.06,30.67]),
    ("北京", "西安",  [116.46,39.92], [108.95,34.27]),
    ("广州", "深圳",  [113.23,23.16], [114.07,22.62]),
    ("武汉", "长沙",  [114.31,30.52], [113.0,28.21]),
    ("上海", "南京",  [121.48,31.22], [118.78,32.04]),
    ("成都", "重庆",  [104.06,30.67], [106.54,29.59]),
]
base_vals = [520, 380, 260, 310, 420, 215, 390, 280]
for i, period in enumerate(periods):
    for j, (fn, tn, fc, tc) in enumerate(routes):
        TOTAL_FLY_DATA.append({
            "fromName": fn, "toName": tn,
            "coords": [fc, tc],
            "value": base_vals[j] + i * 40 + j * 18,
            "type": period
        })
```

---

## 分组柱形地图数据（7大区×3产业 = 21条，按 type 区分）

适用组件：JTotalBarMap

```python
TOTAL_BAR_DATA = []
regions = [
    ("华东",  [121.48, 31.22]),
    ("华南",  [113.23, 23.16]),
    ("华北",  [116.46, 39.92]),
    ("华中",  [114.31, 30.52]),
    ("西南",  [104.06, 30.67]),
    ("东北",  [123.38, 41.80]),
    ("西北",  [108.95, 34.27]),
]
cat_data = {
    "制造业": [28500, 18200, 15600, 22000, 19800, 12000, 10500],
    "服务业": [35800, 24600, 22000, 16500, 13200,  9800,  8200],
    "农业":   [ 4200,  5800,  6100,  8500, 12000,  9200, 15600],
}
for i, (region, coords) in enumerate(regions):
    for cat, vals in cat_data.items():
        TOTAL_BAR_DATA.append({
            "name": region, "value": vals[i], "coords": coords, "type": cat
        })
```

---

## JAreaMap 美化配置（中国地图 option 专项）

> 直接覆盖 `cfg['option']` 和 `cfg['commonOption']`，不要使用 default_configs.json 中的默认值。

```python
# ── option 内部 ──
opt['drillDown'] = False
opt['area'] = {
    'name': ['中国'], 'value': ['china'],
    'markerColor': '#FFD700',
    'shadowBlur': 20, 'shadowColor': '#FFD700',
    'markerCount': 10, 'markerOpacity': 0.9,
    'markerType': 'effectScatter',
    'scatterLabelShow': True,
}
opt['geo'] = {
    'top': 40, 'zoom': 1.1, 'roam': True,
    'itemStyle': {
        'normal': {
            'borderColor': '#1bc8ff', 'areaColor': '#0d2b45',
            'borderWidth': 1, 'shadowBlur': 8,
            'shadowColor': '#1bc8ff80', 'shadowOffsetX': 0, 'shadowOffsetY': 2,
        },
        'emphasis': {'areaColor': '#ffd06690', 'borderWidth': 1}
    },
    'label': {
        'normal': {'color': '#c0e8ff', 'show': True, 'fontSize': 10},
        'emphasis': {'color': '#fff', 'show': True}
    }
}
opt['visualMap'] = {
    'min': 0, 'max': 140000,
    'top': 'bottom', 'left': '3%',
    'calculable': True, 'show': True, 'type': 'continuous',
    'seriesIndex': [0],
    'textStyle': {'color': '#c0e8ff', 'fontSize': 11},
    'inRange': {'color': ['#04387b', '#1565c0', '#1e88e5', '#29b6f6', '#ffd066']}
}
opt['title'] = {
    'show': True, 'text': '标题', 'left': 10,
    'textStyle': {'color': '#e8f4ff', 'fontSize': 16, 'fontWeight': 'bold'}
}

# ── config 顶层 commonOption ──
cfg['commonOption'] = {
    'barSize': 10,
    'gradientColor': True,
    'breadcrumb': {'drillDown': False, 'textColor': '#FFFFFF'},
    'areaColor': {'color1': '#04387b', 'color2': '#ffd066'},
    'barColor': '#29b6f6',
    'barColor2': '#ffd066',
    'inRange': {'color': ['#04387b', '#1e88e5', '#29b6f6', '#ffd066']}
}
```

---

## 各组件 chartData 对应关系速查

| 组件 | 使用数据 | 备注 |
|------|---------|------|
| JBubbleMap | `CITY_SCATTER` | [经度, 纬度, 值] |
| JFlyLineMap | `FLY_LINE_DATA` | fromName/toName/coords/value |
| JBarMap | `CITY_SCATTER` | 同散点，条形高度=值 |
| JHeatMap | `CITY_SCATTER` | 同散点，热力强度=值 |
| JAreaMap | `PROVINCE_GDP` | name 必须匹配 GeoJSON 省名 |
| JTotalFlyLineMap | `TOTAL_FLY_DATA` | 增加 type 字段区分时间段 |
| JTotalBarMap | `TOTAL_BAR_DATA` | 增加 type 字段区分产业类别 |
| JGaoDeMap | 无（默认） | 依赖高德 API Key，不设静态数据 |
