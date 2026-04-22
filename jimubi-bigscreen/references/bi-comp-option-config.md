# 大屏组件配置修改参考

修改大屏组件样式时，根据组件类型和修改目标，使用对应的配置路径。
## 修改输出格式

只返回需要修改的属性，不包含未修改的配置：

```json
{
  "compConfig": {
    "option": {
      "series": [{ "itemStyle": { "color": "#FFFF00" } }]
    }
  }
}
```

修改名称/背景等基础属性：
```json
{
  "compConfig": {
    "name": "京东销量柱形图",
    "background": "#000000"
  }
}
```

## 颜色修改规则

### customColor 组件列表
以下组件的颜色属性使用 `customColor` 格式修改：
- JRadioButton, JRadialBar, JActiveRing, JRing, JPyramidFunnel, JFunnel
- JBubble, DoubleLineBar, JMultipleLine, JArea, JLine
- JRotatePie, JRose, JPie, JMixLineBar, JPercentBar
- JMultipleBar, JCapsuleChart, JStackBar, JQuadrant

格式：
```json
"customColor": [
  {"color1": "#FF0000", "color": "#FF0000"},
  {"color1": "#00FF00", "color": "#00FF00"}
]
```

### 柱体颜色
普通柱状图使用 `option.series[${index}].itemStyle.color`
JDynamicBar 等也使用 `option.series[${index}].itemStyle.color`

### 其他组件
不包含 customColor 属性的组件，按照对应组件配置的属性 value 值修改

## 通用规则

- 颜色使用具体色值（如 `#000000`），不使用英文单词（如 black）
- 字体粗细可选值：`normal`（默认）、`bold`（粗体）、`lighter`（细体）
- Y轴单位 `option.yAxis.yUnit`：预设值有 `%`（百分比）、`K`（千）、`W`（万）、`M`（亿）；自定义单位时设 `yUnit: 'CUSTOM'` 并设 `yCustomUnit: '元'`

## 基础配置 (BasicOption)

| 说明 | 配置路径 |
|------|---------|
| 图层名称 | `name` |
| 图层背景色 | `background` |
| 图层边框线 | `borderColor` |
| 提示语显隐 | `option.tooltip.show` |
| 提示语字体大小 | `option.tooltip.textStyle.fontSize` |
| 提示语字体颜色 | `option.tooltip.textStyle.color` |

## 标题设置 (TitleOption)

| 说明 | 配置路径 |
|------|---------|
| 标题名称 | `option.title.text` |
| 标题字体大小 | `option.title.textStyle.fontSize` |
| 标题字体颜色 | `option.title.textStyle.color` |
| 标题字体粗细 | `option.title.textStyle.fontWeight` |
| 副标题名称 | `option.title.subtext` |
| 副标题字体大小 | `option.title.subtextStyle.fontSize` |
| 副标题字体颜色 | `option.title.subtextStyle.color` |
| 左对齐 | `option.title.left` |
| 垂直居中 | `option.title.top` |

## X轴设置 (XAxisOption)

| 说明 | 配置路径 |
|------|---------|
| X轴名称 | `option.xAxis.name` |
| X轴名称颜色 | `option.xAxis.nameTextStyle.color` |
| X轴名称字体大小 | `option.xAxis.nameTextStyle.fontSize` |
| X轴标签颜色 | `option.xAxis.axisLabel.color` |
| X轴标签角度 | `option.xAxis.axisLabel.rotate` |
| X轴轴线颜色 | `option.xAxis.axisLine.lineStyle.color` |
| X轴类型 | `option.xAxis.type` |
| X轴网格线显隐 | `option.xAxis.splitLine.show` |
| X轴网格线颜色 | `option.xAxis.splitLine.lineStyle.color` |

## Y轴设置 (YAxisOption)

| 说明 | 配置路径 | 备注 |
|------|---------|------|
| Y轴名称 | `option.yAxis.name` | |
| Y轴名称颜色 | `option.yAxis.nameTextStyle.color` | |
| Y轴名称字体大小 | `option.yAxis.nameTextStyle.fontSize` | |
| Y轴标签颜色 | `option.yAxis.axisLabel.color` | |
| Y轴标签角度 | `option.yAxis.axisLabel.rotate` | |
| Y轴轴线颜色 | `option.yAxis.axisLine.lineStyle.color` | |
| Y轴类型 | `option.yAxis.type` | |
| Y轴网格线显隐 | `option.yAxis.splitLine.show` | |
| Y轴网格线颜色 | `option.yAxis.splitLine.lineStyle.color` | |
| Y轴单位 | `option.yAxis.yUnit` | 预设: `%`, `K`, `W`, `M`；自定义: 设为 `CUSTOM` 并设 `yCustomUnit` |

## 图例设置 (LegendOption)

| 说明 | 配置路径 |
|------|---------|
| 图例字体大小 | `option.legend.textStyle.fontSize` |
| 图例排列方向 | `option.legend.orient` |
| 图例上下边距 | `option.legend.t` |
| 图例左右边距 | `option.legend.r` |

## 柱体设置 (BarCylinder)

| 说明 | 配置路径 |
|------|---------|
| 柱体宽度 | `option.series[${index}].barWidth` |
| 柱体圆角 | `option.series[${index}].itemStyle.borderRadius` |
| 柱体颜色 | `option.series[${index}].itemStyle.color` |
| 柱体背景色显隐 | `option.series[${index}].showBackground` |
| 柱体背景色颜色 | `option.series[${index}].backgroundStyle.color` |

## 折线设置 (PolyglineOption)

| 说明 | 配置路径 | 可选值 |
|------|---------|--------|
| 折线类型 | `option.series[${index}].lineType` | `line`（折线）, `smooth`（曲线）, `area`（面积） |
| 透明度 | `option.series[0].areaStyleOpacity` | |
| 线条宽度 | `option.series[${index}].lineWidth` | |
| 标记点 | `option.series[${index}].symbol` | |
| 点的大小 | `option.series[${index}].symbolSize` | |

## 饼图设置 (pieSettingOption)

| 说明 | 配置路径 |
|------|---------|
| 设置成环形 | `option.isRadius` |
| 内环半径 | `option.innerRadius` |
| 外环半径 | `option.outRadius` |
| 南丁格尔玫瑰 | `option.isRose` |
| 标签显示位置 | `option.pieLabelPosition` |

## 坐标轴边距 (GridOption)

| 说明 | 配置路径 |
|------|---------|
| 左边距 | `option.grid.left` |
| 顶边距 | `option.grid.top` |
| 右边距 | `option.grid.right` |
| 底边距 | `option.grid.bottom` |

## 数值设置 (NumOption)

| 说明 | 配置路径 | 可选值 |
|------|---------|--------|
| 显示数值 | `option.series[${index}].label.show` | |
| 数值位置 | `option.series[${index}].label.position` | `top`（顶部）, `""`（中间）, `insideBottom`（底部） |
| 数值格式 | `option.label.format` | |
| 数值颜色 | `option.series[${index}].label.color` | |
| 数值字体大小 | `option.series[${index}].label.fontSize` | |
| 数值字体粗细 | `option.series[${index}].label.fontWeight` | |
| 数值单位显隐 | `option.showUnit.show` | |
| 数值单位数量级 | `option.showUnit.numberLevel` | `1`（百分比）, `3`（千）, `4`（万） |
| 数值单位小数位 | `option.showUnit.decimal` | |

## 文本设置 (TextOption) - JText / JCurrentTime / JNumber 组件

| 说明 | 配置路径 | 可选值 |
|----|---------|--------|
| 字体大小 | `option.body.fontSize` | |
| 字体间距 | `option.body.letterSpacing` | |
| 字体颜色 | `option.body.color` | |
| 字体粗细 | `option.body.fontWeight` | `normal`, `bold`, `lighter` |
| 对齐方式 | `option.body.textAlign` | `left`, `center`, `right` |
| 字体 | `option.body.fontFamily` | |
| 字体风格 | `option.body.fontStyle` | `normal`, `italic` |
| 千分符 | `option.body.thousandSeparator` | |
| 水平间距 | `option.body.marginLeft` | |
| 垂直间距 | `option.body.marginTop` | |
| 跑马灯 | `option.horseLamp` | |
| 跑马灯速度(ms) | `option.speed` | |
| 超链接开关 | `option.isLink` | |
| 超链接地址 | `option.openUrl` | |
| 超链接打开方式 | `option.openType` | `_blank`, `_self` |

### 文本渐变配置（JText / JCurrentTime / JNumber 支持）

| 说明 | 配置路径 | 可选值 |
|------|---------|--------|
| 启用渐变 | `option.body.gradient.enabled` | `true`/`false` |
| 渐变类型 | `option.body.gradient.type` | `linear`（线性）, `radial`（径向） |
| 渐变方向 | `option.body.gradient.direction` | `to right`, `to left`, `to bottom`, `to top`, `135deg` 等 |
| 起始颜色 | `option.body.gradient.startColor` | `#000000` |
| 结束颜色 | `option.body.gradient.endColor` | `#ffffff` |

> **注意**：启用渐变后前端会自动设置 CSS `-webkit-background-clip: text`，`color` 字段将被忽略。

## 翻牌器设置 (CountToTextOption) - JCountTo 组件

| 说明 | 配置路径 |
|------|---------|
| 字体粗细 | `option.fontWeight` |
| 字体颜色 | `option.fontColor` |
| 字体大小 | `option.fontSize` |
| 前缀文本 | `option.prefix` |
| 前缀字体大小 | `option.prefixFontSize` |
| 前缀字体颜色 | `option.prefixColor` |
| 前缀字体粗细 | `option.prefixFontWeight` |
| 前缀对齐方式 | `option.prefixTextAlign` |
| 前缀X间距 | `option.prefixGridX` |
| 前缀Y间距 | `option.prefixGridY` |
| 后缀文本 | `option.suffix` |
| 后缀字体大小 | `option.suffixFontSize` |
| 后缀字体颜色 | `option.suffixColor` |
| 后缀字体粗细 | `option.suffixFontWeight` |
| 后缀对齐方式 | `option.suffixTextAlign` |
| 后缀X间距 | `option.suffixGridX` |
| 后缀Y间距 | `option.suffixGridY` |

## 进度条设置 (CustomProgressOption)

| 说明 | 配置路径 |
|------|---------|
| 目标颜色 | `option.backgroundColor` |
| 进度颜色 | `option.progressColor` |
| 进度条宽度 | `option.barWidth` |
| 边距 | `option.padding` |
| 标题颜色 | `option.titleColor` |
| 标题字体大小 | `option.titleFontSize` |
| 标题位置 | `option.titlePosition` |
| 数值颜色 | `option.valueColor` |
| 数值字体大小 | `option.valueFontSize` |
| 数值位置 | `option.valuePosition` |
| 数值横向偏移 | `option.valueXOffset` |

## 列表进度图设置 (ListProgressOption)

| 说明 | 配置路径 |
|------|---------|
| 行高度 | `option.row.height` |
| 行左边距 | `option.row.marginLeft` |
| 行右边距 | `option.row.marginRight` |
| 行上边距 | `option.row.marginTop` |
| 进度条颜色 | `option.bar.background.color` |
| 进度条填充色 | `option.bar.fill.color` |
| 进度条高度 | `option.bar.height` |
| 进度条圆角 | `option.bar.borderRadius` |
| 指示点大小 | `option.bar.indicatorSize` |
| 指示点颜色 | `option.bar.indicatorColor` |
| 显示边框 | `option.bar.border.enabled` |
| 边框颜色 | `option.bar.border.color` |
| 边框大小 | `option.bar.border.width` |
| 边框边距 | `option.bar.border.padding` |

## 水波图设置 (LiquidPlotOption) - JLiquid 组件

| 说明 | 配置路径 |
|------|---------|
| 显示类型 | `option.liquidType` |
| 波纹颜色 | `option.color` |
| 波纹个数 | `option.count` |
| 波纹长度 | `option.length` |
| 外框颜色 | `option.borderColor` |
| 外框宽度 | `option.borderWidth` |
| 间距 | `option.distance` |
| 透明度 | `option.strokeOpacity` |
| 文本颜色 | `option.textColor` |
| 文本字体大小 | `option.textFontSize` |

## 象形图设置 (PictorialOption) - JPictorialBar 组件

| 说明 | 配置路径 |
|------|---------|
| 柱体颜色 | `option.barColor` |
| 透明度 | `option.barOpacity` |
| 图标间距 | `option.series[0].barCategoryGap` |

## 象形图图标设置 (PictorialIconOption) - JPictorial 组件

| 说明 | 配置路径 |
|------|---------|
| 图标间距 | `option.symbolMargin` |
| 图标大小 | `option.symbolSize` |
| 图标路径/URL | `option.symbol` |

## 仪表盘设置 (GaugeOption)

| 说明 | 配置路径 |
|------|---------|
| 刻度值显隐 | `option.series[0].axisLabel.show` |
| 刻度值颜色 | `option.series[0].axisLabel.color` |
| 刻度值字体大小 | `option.series[0].axisLabel.fontSize` |
| 刻度线显隐 | `option.series[0].axisTick.show` |
| 刻度线长度 | `option.series[0].axisTick.length` |
| 刻度线颜色 | `option.series[0].axisTick.lineStyle.color` |
| 分割线显隐 | `option.series[0].splitLine.show` |
| 分割线长度 | `option.series[0].splitLine.length` |
| 分割线颜色 | `option.series[0].splitLine.lineStyle.color` |
| 指标字号 | `option.series[0].detail.fontSize` |

## 渐变仪表盘设置 (AntvGaugeOption)

| 说明 | 配置路径 |
|------|---------|
| 粗细 | `option.gaugeWidth` |
| 刻度值显隐 | `option.axisLabelShow` |
| 刻度值颜色 | `option.axisLabelColor` |
| 刻度值字体大小 | `option.axisLabelFontSize` |
| 刻度线显隐 | `option.axisTickShow` |
| 刻度线颜色 | `option.lineColor` |
| 文本颜色 | `option.valueColor` |
| 文本字体大小 | `option.valueFontSize` |
| 指针颜色 | `option.indicatorColor` |
| 指针粗细 | `option.indicatorLength` |

## 环形图设置 (ActiveRingPlotOption)

| 说明 | 配置路径 |
|------|---------|
| 颜色 | `option.color` |
| 背景色 | `option.bgColor` |
| 外环半径 | `option.outRadius` |
| 内环半径 | `option.innerRadius` |
| 标题字体大小 | `option.fontSize` |
| 标题字体颜色 | `option.fontColor` |
| 标题字体粗细 | `option.fontWeight` |
| 数值字体大小 | `option.valueFontSize` |
| 数值字体颜色 | `option.valueFontColor` |
| 数值字体粗细 | `option.valueFontWeight` |

## 动态环形图设置 (ActiveRingOption)

| 说明 | 配置路径 |
|------|---------|
| 显示原始值 | `option.showOriginValue` |
| 文字颜色 | `option.textColor` |
| 文字大小 | `option.textFontSize` |
| 线条宽度 | `option.lineWidth` |
| 环半径 | `option.radius` |
| 动态环半径 | `option.activeRadius` |

## 玉珏设置 (RadialBarOption)

| 说明 | 配置路径 |
|------|---------|
| 显示圆角 | `option.radiuShow` |
| 背景显示 | `option.bgShow` |
| 外环半径 | `option.radius` |
| 内环半径 | `option.innerRadius` |
| 最大旋转角 | `option.maxAngle` |

## 矩形图设置 (RectangleOption)

| 说明 | 配置路径 |
|------|---------|
| 文本颜色 | `option.titleColor` |
| 文本字体大小 | `option.titleFontSize` |
| 显示图例 | `option.showLegend` |

## 颜色块设置 (ColorBlockOption)

| 说明 | 配置路径 |
|------|---------|
| 行数 | `option.lineNum` |
| 边距 | `option.padding` |
| X间距 | `option.borderSplitx` |
| Y间距 | `option.borderSplity` |
| 小数位数 | `option.decimals` |
| 字体大小 | `option.fontSize` |
| 字体颜色 | `option.color` |
| 字体粗细 | `option.fontWeight` |
| 对齐方式 | `option.textAlign` |
| 前缀字体颜色 | `option.prefixColor` |
| 前缀字体粗细 | `option.prefixFontWeight` |
| 前缀X间距 | `option.prefixSplitx` |
| 前缀Y间距 | `option.prefixSplity` |
| 后缀字体大小 | `option.suffixFontSize` |
| 后缀字体颜色 | `option.suffixColor` |
| 后缀字体粗细 | `option.suffixFontWeight` |
| 后缀X间距 | `option.suffixSplitx` |

## 字符云设置 (WordCloudOption)

| 说明 | 配置路径 |
|------|---------|
| 字体颜色 | `option.color` |
| 字体间距 | `option.padding` |
| 字体旋转 | `option.rotation` |
| 字体最大值 | `option.minSize` |
| 字体最小值 | `option.maxSize` |
| 形状 | `option.series[0].shape` |

## 闪光云设置 (FlashCloudOption)

| 说明 | 配置路径 |
|------|---------|
| 缩放 | `option.zoom` |
| 字体大小 | `option.textSize` |
| 字体颜色 | `option.textColor` |

## 轮播表格设置 (ScrollBoardOpt) - JScrollBoard 组件

| 说明 | 配置路径 | 可选值 |
|------|---------|--------|
| 轮播方式 | `option.carousel` | `single`（单行）, `page`（整页） |
| 悬浮暂停 | `option.hoverPause` | |
| 等待时间(ms) | `option.waitTime` | |
| 开启排名 | `option.index` | |
| 序号列宽 | `option.indexWidth` | |
| 显示表头 | `option.headShow` | |
| 表头背景颜色 | `option.headerBGC` | |
| 表头行高 | `option.headerHeight` | |
| 表头字体大小 | `option.headFontSize` | |
| 每页行数 | `option.rowNum` | |
| 奇行颜色 | `option.oddRowBGC` | |
| 偶行颜色 | `option.evenRowBGC` | |
| 表体字体大小 | `option.bodyFontSize` | |

## 表格设置 (ScrollTableStyle)

| 说明 | 配置路径 |
|------|---------|
| 开启排名 | `option.ranking` |
| 开启滚动 | `option.scroll` |
| 滚动时间 | `option.scrollTime` |
| 显示表头 | `option.showHead` |
| 表头背景颜色 | `option.headerBgColor` |
| 表头字体颜色 | `option.headerFontColor` |
| 表头字体大小 | `option.fontSize` |
| 行高 | `option.lineHeight` |
| 边框显示 | `option.showBorder` |
| 边框宽度 | `option.borderWidth` |
| 边框颜色 | `option.borderColor` |
| 边框线类型 | `option.borderStyle` |
| 表格字体颜色 | `option.bodyFontColor` |
| 表格字体大小 | `option.bodyFontSize` |
| 奇行颜色 | `option.oddColor` |
| 偶行颜色 | `option.evenColor` |

## 数据表格设置 (TableStyle)

| 说明 | 配置路径 |
|------|---------|
| 表头背景颜色 | `option.headerBgColor` |
| 表头字体大小 | `option.headerFontSize` |
| 表头字体颜色 | `option.headerColor` |
| 内容字体颜色 | `option.bodyColor` |
| 内容字体大小 | `option.bodyFontSize` |
| 内容背景颜色 | `option.bodyBgColor` |

## 列表设置 (ListStyle)

| 说明 | 配置路径 |
|------|---------|
| 显示标题前缀 | `option.showTitlePrefix` |
| 显示时间前缀 | `option.showTimePrefix` |
| 布局 | `option.layout` |
| 标题字体颜色 | `option.titleFontColor` |
| 标题字体粗细 | `option.titleFontWeight` |
| 标题字体大小 | `option.titleFontSize` |
| 图标颜色 | `option.iconColor` |
| 内容颜色 | `option.contentColor` |
| 开启动画 | `option.isEnableAnimation` |
| 轮播时间(ms) | `option.scrollTime` |

## 滚动设置 (ScrollOption) - JScrollRankingBoard 组件

| 说明 | 配置路径 | 可选值 |
|------|---------|--------|
| 是否排序 | `option.sort` | |
| 轮播方式 | `option.carousel` | `single`（单行）, `page`（整页） |
| 显示行数 | `option.rowNum` | |
| 滚动时间(ms) | `option.waitTime` | |
| 进度条颜色 | `option.color` | 默认 `#1370fb` |
| 文字颜色 | `option.textColor` | 默认 `#fff` |
| 字体大小 | `option.fontSize` | 默认 `13` |

## 历程设置 (DevHistoryOption)

| 说明 | 配置路径 |
|------|---------|
| 缩放 | `option.zoom` |
| 轮播间隔 | `option.waitTime` |
| 背景色 | `option.typeBackColor` |
| 字体颜色 | `option.typeFontColor` |
| 内容字体颜色 | `option.titleColor` |
| 内容字体大小 | `option.titleFontSize` |

## 个性排名设置 (RankingStyle) - JFlashList 组件

> ⚠️ **`option.title` 为字符串类型**（不是 ECharts title dict），`option.titleShow` 为独立布尔值控制显隐。
> 禁止将 `title` 转为 `{show, text, textStyle}` 结构，否则模板渲染输出 `[object Object]`。

| 说明 | 配置路径 | 类型 | 备注 |
|------|---------|------|------|
| 整体缩放 | `option.zoom` | number | 范围 1-5 |
| 显示标题 | `option.titleShow` | boolean | 控制标题区域显隐 |
| 标题文本 | `option.title` | **string** | ⚠️ 字符串，非 ECharts title dict |
| 标题颜色 | `option.titleColor` | color | 十六进制色值 |
| 标题字号 | `option.titleSize` | number | 字体大小(px) |
| 排名项名称颜色 | `option.itemColor` | color | 十六进制色值 |
| 数值颜色 | `option.numberColor` | color | 十六进制色值 |
| 数值字号 | `option.numberSize` | number | 字体大小(px) |
| 入场动画类型 | `option.animateType` | string | CSS动画类名，如 `zoomInUp` |

**数据说明**：
- chartData 最多取前 4 条（组件内部 `result.slice(0,4)`），按 value 降序排列
- 字段映射：`name`（排名项名称）、`value`（数值）

## 气泡排名设置 (BubbleRankingStyle)

| 说明 | 配置路径 |
|------|---------|
| 比例 | `option.zoom` |
| 显示提示词 | `option.showTip` |
| 提示词背景颜色 | `option.tipColor` |
| 提示词宽度 | `option.tipWidth` |
| 提示词内容颜色 | `option.tipFontColor` |
| 提示词内容字体大小 | `option.tipFontSize` |

## 滚动列表 (JScrollList)

详细配置见 `references/scroll-list-option-config.md`（变体区分规则、容器/行/表头/序号列/字段映射完整路径 + 三变体 option 示例）。

## 3D金字塔/漏斗设置 (Pyramid3DOption)

| 说明 | 配置路径 |
|------|---------|
| 缩放 | `option.zoom` |
| 尺寸 | `option.size` |

## 圆形进度图设置 (RoundProgressOption) - JRoundProgress 组件

| 说明 | 配置路径 |
|------|---------|
| 背景颜色 | `option.backgroundStyle.color` |
| 外圆边框颜色 | `option.outerCircle.borderColor` |
| 内圆边框颜色 | `option.innerCircle.borderColor` |

## 图片设置 (ImageOption) - JImg 组件

| 说明 | 配置路径 |
|------|---------|
| 图片地址 | `option.body.url` |
| 旋转开关 | `option.izRotate` |
| 旋转时间(ms) | `option.rotateTime` |
| 透明度 | `option.opacity` |
| 背景颜色 | `option.backgroundColor` |
| 圆角 | `option.borderRadius` |
| 内边距 | `option.padding` |

## 图标设置 (CustomIconOption) - JCustomIcon 组件

| 说明 | 配置路径 |
|------|---------|
| 图标颜色 | `option.color` |
| 透明度 | `option.opacity` |
| 模糊度 | `option.filter` |

> `config.type` 设 `'01'`~`'36'` 决定显示哪个系统图标，与 option 无关。

## 轮播图设置 (CarouselOption) - JCarousel 组件

| 说明 | 配置路径 |
|------|---------|
| 自动轮播 | `option.autoplay` |
| 显示指示点 | `option.dots` |
| 指示点位置 | `option.dotPosition` |

## 边框/装饰设置 (BorderDecorationStyle) - JDragBorder / JDragDecoration 组件

| 说明 | 配置路径 |
|------|---------|
| 边框/装饰类型 | `option.type` |
| 标题文本 | `option.title` |
| 主颜色 | `option.mainColor` |
| 副颜色 | `option.subColor` |
| 翻转 | `option.reverse` |
| 动画时长(s) | `option.dur` |
| 扫描动画时长 | `option.scanDur` |
| 光晕动画时长 | `option.haloDur` |

## 播放器设置 (VideoPlayOption) - JVideoPlay 组件

| 说明 | 配置路径 |
|------|---------|
| 自动播放 | `option.autoPlay` |
| 循环播放 | `option.loop` |

## Iframe 设置 (IframeOption) - JIframe 组件

| 说明 | 配置路径 |
|------|---------|
| 链接地址 | `option.body.url` |

## 按钮设置 (RadioButtonStyle) - JRadioButton 组件

| 说明 | 配置路径 | 可选值 |
|------|---------|--------|
| 按钮形状 | `option.body.shape` | |
| 水平间距 | `option.body.marginLeft` | |
| 垂直间距 | `option.body.marginTop` | |

## 天气设置 (WeatherOption) - JWeatherForecast 组件

| 说明 | 配置路径 |
|------|---------|
| 城市 | `option.city` |
| 显示模板 | `option.template` |
| 显示天数 | `option.num` |
| 背景颜色 | `option.bgColor` |
| 字体大小 | `option.fontSize` |
| 字体颜色 | `option.fontColor` |

## 环形设置 (RingOption)

| 说明 | 配置路径 |
|------|---------|
| 内半径 | `option.innerRadius` |
| 外半径 | `option.outRadius` |

## 南丁格尔玫瑰设置 (RoseOption)

| 说明 | 配置路径 |
|------|---------|
| 边框宽度 | `option.series[0].itemStyle.borderWidth` |
| 颜色透明度 | `option.series[0].itemStyle.colorOpacity` |

## 胶囊图设置 (CapsuleChartOption)

| 说明 | 配置路径 |
|------|---------|
| 显示数值 | `option.showValue` |
| X轴名称 | `option.unit` |

## 百分比柱状图样式 (PercentBarStyle)

| 说明 | 配置路径 | 可选值 |
|------|---------|--------|
| Y轴刻度颜色 | `option.yNameFontColor` | |
| Y轴刻度字体大小 | `option.yNameFontSize` | |
| X轴刻度颜色 | `option.xNameFontColor` | |
| X轴刻度字体大小 | `option.xNameFontSize` | |
| 图例位置 | `option.legendPosition` | `top`（居上）, `bottom`（居下） |
| 图例字体颜色 | `option.legendFontColor` | |
| 图例字体大小 | `option.legendFontSize` | |

## 进度条 ECharts 设置 (ProgressOption)

| 说明 | 配置路径 |
|------|---------|
| 显示标题 | `option.yAxis.axisLabel.show` |
| 标题字体颜色 | `option.yAxis.axisLabel.color` |
| 标题字体大小 | `option.yAxis.axisLabel.fontSize` |
| 数值字体颜色 | `option.series[1].label.color` |
| 数值字体大小 | `option.series[1].label.fontSize` |
| 横向偏移 | `option.valueXOffset` |
| 纵向偏移 | `option.valueYOffset` |
| 柱体宽度 | `option.series[0].barWidth` |
| 进度颜色 | `option.series[0].color` |
| 目标颜色 | `option.series[1].color` |

## 地图设置 (MapOption)

| 说明 | 配置路径 |
|------|---------|
| 显示区域名称 | `option.geo.label.normal.show` |
| 区域名称颜色 | `option.geo.label.normal.color` |
| 区域名称字体大小 | `option.geo.label.normal.fontSize` |
| 开启钻取 | `commonOption.breadcrumb.drillDown` |
| 鼠标缩放 | `option.geo.roam` |
| 缩放比例 | `option.geo.zoom` |
| 长宽比 | `option.geo.aspectScale` |
| 顶边距 | `option.geo.top` |
| 左边距 | `option.geo.left` |

## 地图配色设置 (LineMapColorOption)

| 说明 | 配置路径 |
|------|---------|
| 启用渐变色 | `commonOption.gradientColor` |
| 中心颜色 | `commonOption.areaColor.color1` |
| 边缘颜色 | `commonOption.areaColor.color2` |
| 区域颜色 | `commonOption.areaColor.color1` |
| 区域高亮颜色 | `option.geo.itemStyle.emphasis.areaColor` |
| 区域边界颜色 | `option.geo.itemStyle.normal.borderColor` |
| 阴影大小 | `option.geo.itemStyle.normal.shadowBlur` |
| 阴影水平偏移 | `option.geo.itemStyle.normal.shadowOffsetX` |
| 阴影垂直偏移 | `option.geo.itemStyle.normal.shadowOffsetY` |
| 阴影颜色 | `option.geo.itemStyle.normal.shadowColor` |

## 视觉映射设置 (VisualMapOption)

| 说明 | 配置路径 | 可选值 |
|------|---------|--------|
| 开启视觉映射 | `option.visualMap.show` | |
| 类型 | `option.visualMap.type` | `continuous`, `piecewise` |
| 文本颜色 | `option.visualMap.textStyle.color` | |
| 文本粗细 | `option.visualMap.textStyle.fontWeight` | |
| 文本字体大小 | `option.visualMap.textStyle.fontSize` | |
| 最小值 | `option.visualMap.min` | |
| 最大值 | `option.visualMap.max` | |

## 地图散点设置 (ScatterOption)

| 说明 | 配置路径 |
|------|---------|
| 散点大小 | `option.area.markerSize` |
| 散点形状 | `option.area.markerShape` |
| 散点类型 | `option.area.markerType` |
| 散点颜色 | `option.area.markerColor` |
| 散点文本显示 | `option.area.scatterLabelShow` |
| 散点文本颜色 | `option.area.scatterLabelColor` |
| 散点文本位置 | `option.area.scatterLabelPosition` |
| 散点文本字体大小 | `option.area.scatterFontSize` |
| 散点数量 | `option.area.markerCount` |
| 散点透明度 | `option.area.markerOpacity` |

## 热力地图设置 (HeatOption)

| 说明 | 配置路径 |
|------|---------|
| 热力点大小 | `commonOption.heat.pointSize` |
| 模糊大小 | `commonOption.heat.blurSize` |
| 最大透明度 | `commonOption.heat.maxOpacity` |

## 柱体地图设置 (BarMapOption)

| 说明 | 配置路径 |
|------|---------|
| 柱体大小 | `commonOption.barSize` |
| 柱体左侧颜色 | `commonOption.barColor` |
| 柱体右侧颜色 | `commonOption.barColor2` |

## 飞线地图设置 (FlyLineOption)

| 说明 | 配置路径 |
|------|---------|
| 动画时间 | `commonOption.effect.period` |
| 标记形状 | `commonOption.effect.markerShape` |
| 标记大小 | `commonOption.effect.symbolSize` |
| 标记颜色 | `commonOption.effect.markerColor` |
| 尾迹长度 | `commonOption.effect.trailLength` |

---

## 组件数据格式 (chartData)

### 柱状图/折线图/混合图
JBar, JStackBar, JLine, JSmoothLine, JStepLine, JMultipleLine, JArea, JMixLineBar, DoubleLineBar, JHorizontalBar, JBackgroundBar, JMultipleBar, JNegativeBar, JPercentBar
```json
[{"name": "一月", "value": 820, "type": "系列名"}]
```
双轴图额外字段：`"yAxisIndex": "0"` 或 `"1"`

### 饼图/环形图/玫瑰图
JPie, JRose, JRing, JRotatePie, JBreakRing, JActiveRing, JRadialBar, JFunnel, JPyramidFunnel
```json
[{"name": "类别", "value": 800}]
```

### 仪表盘
JGauge, JColorGauge, JAntvGauge
```json
[{"min": 0, "max": 100, "label": "完成率", "value": 76}]
```

### 半圆仪表盘
JSemiGauge
```json
[{"total": 800, "used": 500}]
```

### 水球图
JLiquid（值为 0-100，前端自动除以100）
```json
[{"value": 75}]
```

### 数字指标
JNumber（对象格式，不是数组）
```json
{"value": 128560}
```

### 翻牌器
JCountTo
```json
{"value": 1024}
```

### 文本
JText
```json
{"value": "显示的文字内容"}
```

### 排行榜
JScrollRankingBoard（直接数组，不要 JSON.stringify）
```json
[{"name": "北京", "value": 1200, "type": "城市"}, {"name": "上海", "value": 1050, "type": "城市"}]
```

### 轮播表（二维数组）
JScrollBoard — **chartData 是二维数组**（行 × 列），首行不是表头，表头由 `option.header` 配置：
```json
[
  ["行1列1", "行1列2", "行1列3"],
  ["行2列1", "行2列2", "行2列3"]
]
```
列名通过 `option.header: [{label:"列名", key:"", width:100}]` 配置，`key` 为空时按索引顺序取二维数组值。

### 个性排名
JFlashList（最多取前4条，按 value 降序排列）
```json
[{"name": "苹果", "value": 1000, "type": "手机品牌"}]
```

### 气泡排名
JBubbleRank — **字段为 title/desc，不是 name/value**：
```json
[{"title": "Java", "desc": "事项数：369"}, {"title": "Python", "desc": "事项数：258"}]
```

### 滚动列表
JScrollList — chartData 为业务对象数组，字段名与 `option.fieldMapping[].key` 对应：
```json
[{"plateNumber": "粤A12345", "violationCount": 3}, {"plateNumber": "粤B67890", "violationCount": 1}]
```

### 透视表
JPivotTable — chartData 是复杂对象，不是数组：
```json
{
  "x": [{"fieldId1": ["值A", "值B"]}, {"fieldId2": ["1", "2"]}],
  "data": [
    {"y": ["2022/09", "2022"], "t_id": "rowId1", "data": [111, null], "sum": 111, "summary_col": false}
  ]
}
```

### 滚动表格
JScrollTable（数组 + option.fieldMapping）
```json
[{"col1": "值1", "col2": "值2"}]
```
option 需配合 `fieldMapping: [{"name": "列名", "key": "col1", "width": "30%"}]`

### 数据表格
JTable, JCommonTable
```json
[
  {"fieldTxt": "姓名", "fieldName": "name", "type": "field", "isShow": "Y"},
  {"fieldTxt": "年龄", "fieldName": "age", "type": "field", "isShow": "Y"}
]
```

### 数据列表
JList
```json
[{"title": "标题", "date": "2026-03-18", "desc": "描述", "avatar": "url"}]
```

### 词云
JWordCloud, JImgWordCloud, JFlashCloud
```json
[{"name": "关键词", "value": 100}]
```

### 地图组件
JAreaMap, JBubbleMap, JFlyLineMap, JBarMap, JHeatMap
```json
[{"name": "城市名", "value": 199}]
```

### 按钮
JRadioButton, JCustomButton
```json
[{"title": "按钮文字", "value": 0, "href": "https://example.com"}]
```

### 轮播图
JCarousel
```json
[{"src": "https://example.com/1.png"}, {"src": "https://example.com/2.png"}]
```

### 进度条
JProgress
```json
[{"name": "任务A", "value": 80, "total": 100}]
```

### 胶囊图
JCapsuleChart
```json
[{"name": "类目", "value": 500}]
```

### 性别比例
JGender
```json
[{"man": 60, "woman": 40}]
```

### 统计卡片
JStatsSummary
```json
[{"title": "指标名", "value": 1234, "unit": "元", "compare": 12.5, "label": "同比", "state": "up"}]
```

---

## 组件与设置面板映射表

每个组件在设计器右侧面板显示的配置项列表（optionList），以下为完整映射：

### 柱状图系列
| 组件 | 设置面板 |
|------|---------|
| JBar | BasicOption, TitleOption, XAxisOption, YAxisOption, LegendOption, GridOption, NumOption, BarCylinder, CustomColorOption, OtherOption |
| JStackBar | BasicOption, TitleOption, XAxisOption, YAxisOption, LegendOption, GridOption, NumOption, BarCylinder, CustomColorOption |
| JDynamicBar | BasicOption, TitleOption, XAxisOption, YAxisOption, GridOption, BarCylinder |
| JHorizontalBar | BasicOption, TitleOption, XAxisOption, YAxisOption, LegendOption, GridOption, NumOption, BarCylinder, CustomColorOption |
| JBackgroundBar | BasicOption, TitleOption, XAxisOption, YAxisOption, GridOption, NumOption, BarCylinder |
| JMultipleBar | BasicOption, TitleOption, XAxisOption, YAxisOption, LegendOption, GridOption, NumOption, BarCylinder, CustomColorOption |
| JNegativeBar | BasicOption, TitleOption, XAxisOption, YAxisOption, LegendOption, GridOption, CustomColorOption |
| JPercentBar | BasicOption, PercentBarStyle, CustomColorOption |
| JCapsuleChart | BasicOption, CapsuleChartOption, CustomColorOption |

### 折线/面积图系列
| 组件 | 设置面板 |
|------|---------|
| JLine | BasicOption, TitleOption, XAxisOption, YAxisOption, LegendOption, GridOption, NumOption, PolyglineOption, CustomColorOption, OtherOption |
| JSmoothLine | BasicOption, TitleOption, XAxisOption, YAxisOption, LegendOption, GridOption, NumOption, PolyglineOption |
| JStepLine | BasicOption, TitleOption, XAxisOption, YAxisOption, LegendOption, GridOption, NumOption |
| JArea | BasicOption, TitleOption, XAxisOption, YAxisOption, LegendOption, GridOption, NumOption, PolyglineOption, CustomColorOption |
| JMultipleLine | BasicOption, TitleOption, XAxisOption, YAxisOption, LegendOption, GridOption, NumOption, PolyglineOption, CustomColorOption |

### 混合图系列
| 组件 | 设置面板 |
|------|---------|
| JMixLineBar | BasicOption, TitleOption, XAxisOption, YAxisOption, LegendOption, GridOption, NumOption, BarCylinder, PolyglineOption, CustomColorOption |
| DoubleLineBar | BasicOption, TitleOption, XAxisOption, YLeftAxisOption, YRightAxisOption, LegendOption, GridOption, NumOption, BarCylinder, PolyglineOption, CustomColorOption |

### 饼图/环形图系列
| 组件 | 设置面板 |
|------|---------|
| JPie | BasicOption, TitleOption, LegendOption, gridPieOption, pieSettingOption, NumOption, CustomColorOption |
| JRose | BasicOption, TitleOption, LegendOption, gridPieOption, RoseOption, NumOption, CustomColorOption |
| JRotatePie | BasicOption, TitleOption, LegendOption, gridPieOption, CustomColorOption |
| JRing | BasicOption, TitleOption, LegendOption, gridPieOption, RingOption, NumOption, CustomColorOption |
| JBreakRing | BasicOption, BreakRingOption |
| JActiveRing | BasicOption, ActiveRingOption, CustomColorOption |
| JRadialBar | BasicOption, RadialBarOption, CustomColorOption |

### 仪表/进度系列
| 组件 | 设置面板 |
|------|---------|
| JGauge | BasicOption, GaugeOption, CustomColorOption |
| JColorGauge | BasicOption, GaugeOption, CustomColorOption |
| JAntvGauge | BasicOption, AntvGaugeOption, CustomColorOption |
| JSemiGauge | BasicOption, SemiGaugeOption |
| JProgress | BasicOption, ProgressOption, CustomColorOption |
| JCustomProgress | BasicOption, CustomProgressOption |
| JListProgress | BasicOption, ListProgressOption |
| JRoundProgress | BasicOption, RoundProgressOption |
| JRingProgress | BasicOption, ActiveRingPlotOption |
| JLiquid | BasicOption, LiquidPlotOption |

### 散点/气泡/漏斗系列
| 组件 | 设置面板 |
|------|---------|
| JScatter | BasicOption, TitleOption, XAxisOption, YAxisOption, LegendOption, GridOption |
| JBubble | BasicOption, TitleOption, XAxisOption, YAxisOption, LegendOption, GridOption, CustomColorOption |
| JQuadrant | BasicOption, TitleOption, XAxisOption, YAxisOption, LegendOption, GridOption, CustomColorOption |
| JFunnel | BasicOption, TitleOption, LegendOption, NumOption, CustomColorOption |
| JPyramidFunnel | BasicOption, TitleOption, LegendOption, NumOption, CustomColorOption |
| JPyramid3D | BasicOption, Pyramid3DOption, CustomColorOption |
| JRadar | BasicOption, TitleOption, LegendOption, CustomColorOption |

### 文本/数字系列
| 组件 | 设置面板 |
|------|---------|
| JText | BasicOption, TextOption, ModalSettingsOption |
| JCountTo | BasicOption, CountToTextOption |
| JNumber | BasicOption, TextOption |
| JColorBlock | BasicOption, ColorBlockOption |
| JCurrentTime | BasicOption, TextOption |

### 表格/列表系列
| 组件 | 设置面板 |
|------|---------|
| JScrollBoard | BasicOption, ScrollBoardOpt |
| JScrollTable | BasicOption, ScrollTableStyle |
| JCommonTable | BasicOption, TableStyle |
| JTable | BasicOption, TableStyle |
| JList | BasicOption, ListStyle |
| JScrollList | BasicOption, ScrollListOption |
| JScrollRankingBoard | BasicOption, ScrollOption |
| JFlashList | BasicOption |
| JBubbleRank | BasicOption, BubbleRankingStyle |
| JDevHistory | BasicOption, DevHistoryOption |

### 地图系列
| 组件 | 设置面板 |
|------|---------|
| JAreaMap | BasicOption, MapOption, LineMapColorOption, VisualMapOptoin |
| JBubbleMap | BasicOption, MapOption, LineMapColorOption, ScatterOption, VisualMapOptoin |
| JFlyLineMap | BasicOption, MapOption, LineMapColorOption, FlyLineOption, ScatterOption |
| JBarMap | BasicOption, MapOption, LineMapColorOption, BarMapOption |
| JHeatMap | BasicOption, MapOption, LineMapColorOption, HeatOption |
| JTotalFlyLineMap | BasicOption, MapOption, LineMapColorOption, FlyLineOption, ScatterOption, TimeLineOption |
| JTotalBarMap | BasicOption, MapOption, LineMapColorOption, BarMapOption, TimeLineOption |

### 其他组件
| 组件 | 设置面板 |
|------|---------|
| JWordCloud | BasicOption, WordCloudOption, CustomColorOption |
| JImgWordCloud | BasicOption, WordCloudOption |
| JFlashCloud | BasicOption, FlashCloudOption |
| JRadioButton | BasicOption, RadioButtonStyle, CustomColorOption |
| JSelectRadio | BasicOption, TabSelectOption |
| JPictorialBar | BasicOption, TitleOption, YAxisOption, XAxisOption, GridOption, PictorialOption, OtherOption |
| JPictorial | BasicOption, TitleOption, XAxisOption, YAxisOption, GridOption, PictorialIconOption, OtherOption |
| JGender | BasicOption, LegendOption |
| JStatsSummary | BasicOption, StatsSummaryOption |
| JCarousel | BasicOption, CarouselOption |
| JVideoPlay | BasicOption, VideoPlayOption |
| JIframe | BasicOption, IframeOption |
| JRectangle | BasicOption, RectangleOption |
| JImg | BasicOption, ImageOption |
| JCustomIcon | BasicOption, customIconOption |
| JWeatherForecast | BasicOption, WeatherOption |
| JDragBorder | BasicOption, BorderDecorationStyle |
| JDragDecoration | BasicOption, BorderDecorationStyle |
| JRoundProgress | BasicOption, RoundProgressOption |

---

## ECharts 与非 ECharts 组件区分

**ECharts 组件**（底层用 ECharts 渲染，option 遵循 ECharts 规范 + 扩展属性）：
JBar, JStackBar, JDynamicBar, JHorizontalBar, JBackgroundBar, JMultipleBar, JNegativeBar,
JLine, JSmoothLine, JStepLine, JMultipleLine, JArea,
JMixLineBar, DoubleLineBar,
JPie, JRose, JRotatePie, JRing,
JScatter, JBubble, JQuadrant,
JFunnel, JPyramidFunnel,
JRadar, JCircleRadar,
JGauge, JColorGauge,
JProgress, JPictorialBar,
JBar3d, JBarGroup3d,
JWordCloud,
JAreaMap, JBubbleMap, JFlyLineMap, JBarMap, JHeatMap, JTotalFlyLineMap, JTotalBarMap,
JCustomEchart

**非 ECharts 组件**（自定义渲染，option 使用组件私有属性）：
JNumber, JCountTo, JText, JColorBlock, JCurrentTime,
JLiquid, JAntvGauge, JSemiGauge, JCustomProgress, JListProgress, JRoundProgress, JRingProgress,
JActiveRing, JRadialBar, JBreakRing,
JCapsuleChart, JPercentBar,
JScrollBoard, JScrollTable, JCommonTable, JTable, JList, JScrollList, JScrollRankingBoard, JFlashList, JBubbleRank,
JCarousel, JVideoPlay, JImg, JIframe,
JRadioButton, JSelectRadio, JTabToggle, JForm,
JDragBorder, JDragDecoration, JDragEditor,
JPyramid3D, JGender, JStatsSummary,
JFlashCloud, JImgWordCloud, JOrbitRing, JRectangle, JDevHistory
