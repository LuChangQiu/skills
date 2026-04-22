# JTabToggle（导航切换）配置路径

> 来源：`TabToggleOption.vue`（配置面板）+ `TabToggle.vue`（渲染逻辑）
>
> 用途：点击/自动轮播切换高亮项，同时控制页面其他组件的显示/隐藏，实现多页面导航效果。

## 基础配置

| 说明 | 配置路径 | 默认值 |
|------|---------|--------|
| 自动轮播 | `option.autoPlay` | `false` |
| 轮播时间（秒） | `option.time` | `60`；autoPlay=true 时生效 |
| 个性化模式（每项独立图片） | `option.personalizedMode` | `false` |
| 当前高亮项 value | `option.currentValue` | 第一项的 value |

## 通用样式（option.normal，普通态）

| 说明 | 配置路径 | 默认值 |
|------|---------|--------|
| 字号 | `option.normal.fontSize` | `16` |
| 字重 | `option.normal.fontWeight` | `normal` / `bold` / `lighter` |
| 字体风格 | `option.normal.fontStyle` | `normal` / `italic` |
| 文字颜色 | `option.normal.color` | `#d8d8d8` |
| 背景色 | `option.normal.backgroundColor` | `#3a414d` |
| 边框颜色 | `option.normal.borderColor` | `""` |
| 边框宽度 | `option.normal.borderWidth` | `0` |
| 背景图片 URL | `option.normal.imgUrl` | `""` |
| 背景图片大小 | `option.normal.backgroundSize` | `100% 100%`（拉伸铺满）/ `cover` / `contain` / `auto` |
| 背景图片重复 | `option.normal.backgroundRepeat` | `no-repeat` / `repeat` / `repeat-x` / `repeat-y` |
| 背景图片位置 | `option.normal.backgroundPosition` | `center center` / `left top` 等 |
| 渐变启用（文字） | `option.normal.gradient.enabled` | `false` |
| 渐变类型 | `option.normal.gradient.type` | `linear` / `radial` |
| 渐变方向 | `option.normal.gradient.direction` | `to right` |
| 渐变起始色 | `option.normal.gradient.startColor` | `#000000` |
| 渐变结束色 | `option.normal.gradient.endColor` | `#FFFFFF` |

> `option.normal.imgUrl` 和 `option.personalizedMode` 任一为真时，背景图片的 `backgroundSize/Repeat/Position` 才会渲染。

## 高亮样式（option.active，高亮/选中态）

| 说明 | 配置路径 | 默认值 |
|------|---------|--------|
| 字号 | `option.active.fontSize` | `16` |
| 字重 | `option.active.fontWeight` | 继承 `option.normal.fontWeight` |
| 字体风格 | `option.active.fontStyle` | 继承 `option.normal.fontStyle` |
| 文字颜色 | `option.active.color` | `#ffffff` |
| 背景色 | `option.active.backgroundColor` | `#0a73ff` |
| 边框颜色 | `option.active.borderColor` | `""` |
| 边框宽度 | `option.active.borderWidth` | `0` |
| 背景图片 URL | `option.active.imgUrl` | `""` |
| 背景图片大小 | `option.active.backgroundSize` | `100% 100%` |
| 背景图片重复 | `option.active.backgroundRepeat` | `no-repeat` |
| 背景图片位置 | `option.active.backgroundPosition` | `center center` |
| 渐变启用（文字） | `option.active.gradient.enabled` | `false` |
| 渐变类型 | `option.active.gradient.type` | `linear` / `radial` |
| 渐变方向 | `option.active.gradient.direction` | `to right` |
| 渐变起始色 | `option.active.gradient.startColor` | `#000000` |
| 渐变结束色 | `option.active.gradient.endColor` | `#FFFFFF` |

## 项目配置（option.items）

`option.items` 是数组，每项对应一个导航 Tab。

| 说明 | 配置路径 | 示例值 |
|------|---------|--------|
| 显示文字 | `option.items[i].label` | `销售概览` |
| 唯一标识（联动用） | `option.items[i].value` | `sales` |
| 切换时显示的组件 ID 列表 | `option.items[i].compVals` | `["comp_id_1", "comp_id_2"]` |

### 个性化模式专有字段（personalizedMode=true）

| 说明 | 配置路径 | 示例值 |
|------|---------|--------|
| 常态图片 URL | `option.items[i].normalImgUrl` | `""` |
| 高亮图片 URL | `option.items[i].activeImgUrl` | `""` |
| 自定义宽度（px，0=auto） | `option.items[i].width` | `0` |
| 左边距 | `option.items[i].marginLeft` | `0` |
| 右边距 | `option.items[i].marginRight` | `0` |
| 上边距 | `option.items[i].marginTop` | `0` |
| 下边距 | `option.items[i].marginBottom` | `0` |

> `compVals` 为空数组时该项不控制任何组件显隐；配置后，切换到该项时指定组件显示，其他项的 compVals 中包含的组件隐藏。

## chartData 格式

```python
chart_data = [
    {"label": "销售概览", "value": "sales"},
    {"label": "库存管理", "value": "inventory"},
    {"label": "客户分析", "value": "customer"},
    {"label": "财务报表", "value": "finance"},
]
# label=显示文字，value=唯一标识
```

## 完整 option 示例

```python
option = {
    "autoPlay": True,
    "time": 5,
    "personalizedMode": False,
    "currentValue": "sales",
    "normal": {
        "fontSize": 14,
        "fontWeight": "normal",
        "fontStyle": "normal",
        "color": "#d8d8d8",
        "backgroundColor": "#1e2a3a",
        "borderColor": "#2b4c6f",
        "borderWidth": 1,
        "imgUrl": "",
        "backgroundSize": "100% 100%",
        "backgroundRepeat": "no-repeat",
        "backgroundPosition": "center center",
        "gradient": {"enabled": False},
    },
    "active": {
        "fontSize": 14,
        "fontWeight": "bold",
        "fontStyle": "normal",
        "color": "#ffffff",
        "backgroundColor": "#0a73ff",
        "borderColor": "#40a9ff",
        "borderWidth": 1,
        "imgUrl": "",
        "backgroundSize": "100% 100%",
        "backgroundRepeat": "no-repeat",
        "backgroundPosition": "center center",
        "gradient": {"enabled": False},
    },
    "items": [
        {"label": "销售概览", "value": "sales",     "compVals": ["comp_id_1"]},
        {"label": "库存管理", "value": "inventory", "compVals": ["comp_id_2"]},
        {"label": "客户分析", "value": "customer",  "compVals": ["comp_id_3"]},
    ],
}
```
