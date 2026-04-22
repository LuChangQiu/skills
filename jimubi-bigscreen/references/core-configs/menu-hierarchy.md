# 大屏组件菜单层级结构

> 提取自 `packages/dragEngine/components/bigScreenComponents/data.ts` 的 `menuData` 导出。
> 此文件记录组件面板的完整分类树，用于理解组件归属和定位。

---

## 一级分类（6个顶层 Tab）

```
menuData [
  {id:'200',                    name:'图表',    compType:'chart'}
  {id:'300000',                 name:'文字',    compType:'text'}
  {id:'707153616621699072',     name:'自定义',  compType:'customForm'}
  {id:'100120100200',           name:'地图',    compType:'mapMenu'}
  {id:'1009728871115423744',    name:'视频',    compType:'video'}   ← 含边框/装饰/视频
  {id:'100',                    name:'其他',    compType:'JSelectRadio'}
]
```

> ⚠️ **注意**：`视频` Tab（id:1009728871115423744）实际包含 **边框+装饰+视频** 三类组件，命名具有误导性。
> ⚠️ **注意**：进度图子节点在源码中 `parentId` 误写为 `'200'`，实际属于进度图分组（按数组嵌套结构判断）。

---

## 完整层级树

### 图表 (id:200)

```
图表
├── 柱形图 (id:200200)
│   ├── JBar           基础柱形图
│   ├── JStackBar      堆叠柱形图
│   ├── JDynamicBar    动态柱形图
│   ├── JCapsuleChart  胶囊图
│   ├── JHorizontalBar 基础条形图
│   ├── JBackgroundBar 背景柱形图
│   ├── JMultipleBar   对比柱形图
│   ├── JNegativeBar   正负条形图
│   ├── JPercentBar    百分比条形图
│   └── JMixLineBar    折柱图
│
├── 饼状图 (id:200201)
│   ├── JPie           饼图
│   ├── JRose          南丁格尔玫瑰图
│   └── JRotatePie     旋转饼图
│
├── 折线图 (id:1537002903949037570)
│   ├── JLine          基础折线图
│   ├── JSmoothLine    平滑曲线图
│   ├── JStepLine      阶梯折线图
│   ├── JArea          面积图
│   ├── JMultipleLine  对比折线图
│   └── DoubleLineBar  双轴图
│
├── 进度图 (id:15341365037570)
│   ├── JCustomProgress  基础进度图
│   ├── JProgress        进度图
│   ├── JListProgress    列表进度图
│   ├── JRoundProgress   圆形进度图
│   └── JLiquid          水波图
│
├── 象形图 (id:15311165037570)
│   ├── JPictorialBar  象形柱图
│   ├── JPictorial     象形图
│   └── JGender        男女占比
│
├── 仪表盘 (id:200300)
│   ├── JGauge         基础仪表盘
│   ├── JColorGauge    多色仪表盘
│   ├── JAntvGauge     渐变仪表盘
│   └── JSemiGauge     半圆仪表盘
│
├── 散点图 (id:1537764165146476546)
│   ├── JScatter       普通散点图
│   ├── JQuadrant      象限图
│   └── JBubble        气泡图
│
├── 漏斗图 (id:1537764868216684545)
│   ├── JFunnel        普通漏斗图
│   ├── JPyramidFunnel 金字塔漏斗图
│   └── JPyramid3D     3D金字塔
│
├── 雷达图 (id:1537773378102984706)
│   ├── JRadar         普通雷达图
│   └── JCircleRadar   圆形雷达图
│
├── 环形图 (id:1534136503807570)
│   ├── JRing          饼状环形图
│   ├── JBreakRing     多色环形图
│   ├── JRingProgress  基础环形图
│   ├── JActiveRing    动态环形图
│   └── JRadialBar     玉珏图
│
├── 矩形图 (id:153413650123456)
│   └── JRectangle     矩形图
│
├── 3D图表 (id:1735280687890)
│   ├── JBar3d         3D柱形图
│   └── JBarGroup3d    3D分组柱形图
│
├── 日历 (id:1735280687892)
│   └── JPermanentCalendar  日历
│
├── 轮播 (id:1756869717059)
│   ├── JCardScroll index=0  卡片滚动(横向)
│   ├── JCardScroll index=1  卡片滚动(竖向+序号)
│   ├── JCardScroll index=2  卡片滚动(高亮)
│   └── JCardCarousel        卡片轮播
│
├── 统计 (id:1762849143133)
│   ├── JStatsSummary index=0  统计概览（卡片模式）
│   ├── JStatsSummary index=1  统计概览（背景模式）
│   └── JStatsSummary index=2  统计概览（高亮模式）
│
├── 装饰 (id:15341365037580)
│   └── JCustomIcon  图标（36种，type='01'~'36'）
│
└── 表格 (id:400000)
    ├── 轮播表格
    │   ├── JScrollBoard      轮播表
    │   ├── JScrollTable      表格
    │   └── JDevHistory       发展历程
    ├── 普通表格
    │   ├── JCommonTable      数据表格
    │   └── JList             数据列表
    ├── 排名表格
    │   ├── JScrollRankingBoard  排行榜
    │   ├── JFlashList           个性排名(前四)
    │   └── JBubbleRank          气泡排名(前五)
    └── 高级表格
        ├── JScrollList index=0  滚动列表(单行)
        ├── JScrollList index=1  滚动列表(多行+序号)
        └── JScrollList index=2  滚动列表(带表头)
```

### 文字 (id:300000)

```
文字
├── 文本类 (id:300000100)
│   ├── JText         文本
│   ├── JCountTo      翻牌器
│   ├── JColorBlock   颜色块
│   ├── JCurrentTime  当前时间
│   ├── JNumber       数值
│   └── JOrbitRing    轨道环形文字
│
├── 字符云 (id:300000200)
│   ├── JWordCloud    字符云
│   ├── JImgWordCloud 图层字符云
│   └── JFlashCloud   闪动字符云
│
└── 天气预报 (id:300000300)
    ├── JWeatherForecast template=11   滚动版 (311×47)
    ├── JWeatherForecast template=34   横线版 (300×30)
    ├── JWeatherForecast template=21   带背景 (415×131)
    ├── JWeatherForecast template=12   好123版 (318×61)
    ├── JWeatherForecast template=27   温度计版 (400×266)
    └── JWeatherForecast template=94   列表文字版 (257×47)
```

### 自定义 (id:707153616621699072)

```
自定义
├── Online表单   (id:715067888995565568, compType:online)   ← 动态加载Online表单图表
├── 设计器表单   (id:732470878136074240, compType:design)   ← 动态加载设计器表单图表
├── JTotalProgress  统计进度图
├── JPivotTable     透视表
└── JRankingList    排行榜(自定义)
```

### 地图 (id:100120100200)

```
地图
├── 离线地图 (id:100120100200320)
│   ├── JBubbleMap       散点地图
│   ├── JFlyLineMap      飞线地图
│   ├── JBarMap          柱形地图
│   ├── JTotalFlyLineMap 时间轴飞线地图
│   ├── JTotalBarMap     柱形排名地图
│   ├── JHeatMap         热力地图
│   ├── JAreaMap         区域地图
│   └── JGaoDeMap        高德地图
│
└── 在线地图 (id:1757055654971)   ← 暂无子组件
```

### 视频 (id:1009728871115423744)

> ⚠️ 该 Tab 命名为"视频"，但实际包含边框、装饰和视频三类。

```
视频
├── 边框 (id:1009728983979950080)
│   └── JDragBorder type='1'~'13'   边框1~13
│
├── 装饰 (id:1009729002476830720)
│   └── JDragDecoration type='1'~'12'   装饰1~12
│
└── 视频 (id:610000)
    ├── JVideoPlay   播放器
    └── JVideoJs     RTMP播放器
```

### 其他 (id:100)

```
其他
├── JSelectRadio    选项卡
├── JTabToggle      导航切换
├── JForm           表单
├── JIframe         Iframe
├── JRadioButton    按钮
├── JDragEditor     富文本
├── JCommon         通用组件
└── JCustomEchart   自定义组件
```

---

## 组件总数统计

| 分类 | 组件数 | compType 列表 |
|------|--------|--------------|
| 柱形图 | 10 | JBar/JStackBar/JDynamicBar/JCapsuleChart/JHorizontalBar/JBackgroundBar/JMultipleBar/JNegativeBar/JPercentBar/JMixLineBar |
| 饼状图 | 3 | JPie/JRose/JRotatePie |
| 折线图 | 6 | JLine/JSmoothLine/JStepLine/JArea/JMultipleLine/DoubleLineBar |
| 进度图 | 5 | JCustomProgress/JProgress/JListProgress/JRoundProgress/JLiquid |
| 象形图 | 3 | JPictorialBar/JPictorial/JGender |
| 仪表盘 | 4 | JGauge/JColorGauge/JAntvGauge/JSemiGauge |
| 散点图 | 3 | JScatter/JQuadrant/JBubble |
| 漏斗图 | 3 | JFunnel/JPyramidFunnel/JPyramid3D |
| 雷达图 | 2 | JRadar/JCircleRadar |
| 环形图 | 5 | JRing/JBreakRing/JRingProgress/JActiveRing/JRadialBar |
| 矩形图 | 1 | JRectangle |
| 3D图表 | 2 | JBar3d/JBarGroup3d |
| 日历 | 1 | JPermanentCalendar |
| 轮播/卡片 | 4 | JCardScroll(×3变体)/JCardCarousel |
| 统计概览 | 3 | JStatsSummary(×3变体) |
| 图标 | 1 | JCustomIcon（36种type） |
| 轮播表格 | 3 | JScrollBoard/JScrollTable/JDevHistory |
| 普通表格 | 2 | JCommonTable/JList |
| 排名表格 | 3 | JScrollRankingBoard/JFlashList/JBubbleRank |
| 高级表格 | 3 | JScrollList(×3变体) |
| 文字 | 6 | JText/JCountTo/JColorBlock/JCurrentTime/JNumber/JOrbitRing |
| 字符云 | 3 | JWordCloud/JImgWordCloud/JFlashCloud |
| 天气预报 | 6 | JWeatherForecast(×6变体，template不同) |
| 自定义 | 3 | JTotalProgress/JPivotTable/JRankingList |
| 地图 | 8 | JBubbleMap/JFlyLineMap/JBarMap/JTotalFlyLineMap/JTotalBarMap/JHeatMap/JAreaMap/JGaoDeMap |
| 边框 | 13 | JDragBorder(type='1'~'13') |
| 装饰 | 12 | JDragDecoration(type='1'~'12') |
| 视频 | 2 | JVideoPlay/JVideoJs |
| 其他/交互 | 8 | JSelectRadio/JTabToggle/JForm/JIframe/JRadioButton/JDragEditor/JCommon/JCustomEchart |
| **总计** | **~129 实例** | **~85 compType**（含同 compType 多变体） |
