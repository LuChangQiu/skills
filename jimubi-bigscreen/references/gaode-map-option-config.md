# JGaoDeMap（高德地图）配置路径

> 来源：`GaoDeMapSettings.vue`（配置面板）+ `GaoDeMap.vue`（渲染逻辑）
>
> 注意：JGaoDeMap 使用高德地图 JavaScript API，需要在项目中配置高德地图 Key。

## 中心坐标

| 说明 | 配置路径 | 默认值 |
|------|---------|--------|
| 中心点经度 | `option.center_longitude` | `116.397428`（北京天安门） |
| 中心点纬度 | `option.center_latitude` | `39.90923` |

## 地图样式（option.mapStyle）

| 说明 | 配置路径 | 枚举值 |
|------|---------|--------|
| 地图主题 | `option.mapStyle` | `normal`（标准）/ `dark`（深色）/ `light`（浅色）/ `whitesmoke`（白烟）/ `fresh`（清新）/ `grey`（灰色）/ `graffiti`（涂鸦）/ `macaron`（马卡龙）/ `blue`（蓝色）/ `darkblue`（深蓝）/ `wine`（酒红） |

> 大屏场景推荐使用 `dark`、`darkblue`、`blue` 等深色主题。

## 地图显示要素（option.features）

`option.features` 是数组，控制地图上显示哪些要素：

| 要素值 | 说明 |
|--------|------|
| `bg` | 背景面（显示区域底色） |
| `road` | 道路 |
| `building` | 建筑物（3D模式下有立体效果） |
| `point` | 兴趣点（地标、商铺等） |

```python
# 显示全部要素
option["features"] = ["bg", "road", "building", "point"]

# 仅显示背景和道路（简洁风格）
option["features"] = ["bg", "road"]
```

## 视图模式（option.viewMode）

| 说明 | 配置路径 | 枚举值 |
|------|---------|--------|
| 视图维度 | `option.viewMode` | `2D` / `3D` |

> 3D 模式下 `pitch`（俯仰角）才会生效。

## 缩放配置

| 说明 | 配置路径 | 默认值 |
|------|---------|--------|
| 初始缩放级别 | `option.zoom` | `15` |
| 最小缩放级别 | `option.minZoom` | `2` |
| 最大缩放级别 | `option.maxZoom` | `26` |

> 常用缩放参考：全国视图约 4-5，省级约 7-8，城市约 11-13，区县约 14-15，街道约 16-17。

## 旋转与俯仰

| 说明 | 配置路径 | 范围 / 默认值 |
|------|---------|--------------|
| 地图旋转角度 | `option.rotation` | `0`~`360`，默认 `0` |
| 俯仰角（3D模式） | `option.pitch` | `0`~`90`，默认 `0`；viewMode=3D 时生效 |

## 常用城市坐标参考

| 城市 | 经度 | 纬度 |
|------|------|------|
| 北京 | `116.397428` | `39.90923` |
| 上海 | `121.473701` | `31.230416` |
| 广州 | `113.264385` | `23.129112` |
| 深圳 | `114.057868` | `22.543099` |
| 杭州 | `120.153576` | `30.287459` |
| 成都 | `104.065735` | `30.659462` |
| 武汉 | `114.298572` | `30.584355` |
| 南京 | `118.796877` | `32.060255` |

## 完整 option 示例

```python
option = {
    "center_longitude": 116.397428,
    "center_latitude": 39.90923,
    "mapStyle": "darkblue",
    "features": ["bg", "road", "building", "point"],
    "viewMode": "3D",
    "zoom": 13,
    "minZoom": 2,
    "maxZoom": 26,
    "rotation": 0,
    "pitch": 45,  # 3D模式下的俯仰角
}
```

## chartData 格式

JGaoDeMap 通常不需要 chartData，地图上的标记点/热力层通过数据集绑定传入，数据字段一般包含 `longitude`（经度）、`latitude`（纬度）、`value`（数值）、`name`（名称）等。

```python
# 空数据（仅展示底图）
chart_data = []

# 带标记点数据
chart_data = [
    {"name": "总部", "longitude": 116.397428, "latitude": 39.90923, "value": 100},
    {"name": "分部", "longitude": 121.473701, "latitude": 31.230416, "value": 80},
]
```
