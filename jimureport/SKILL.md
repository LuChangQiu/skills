---
name: jimureport
description: 积木报表生成器 — 自然语言描述报表需求或提供截图，自动生成积木报表（支持数据报表、打印报表、分组报表、循环报表、数据填报等全类型）。Use when user says "积木报表", "jmreport", "Excel报表", "数据填报", "可视化报表", "打印报表", "分组报表", "循环报表", "按照截图生成报表", "创建积木报表", "做一个可视化报表", "积木设计器", "create jimureport", "visual report". Also triggers when user describes report requirements involving Excel-like layouts, data binding with #{}, or multi-sheet reports, or provides a screenshot to generate a report.
---

# 积木报表 AI 生成器

> 不涉及「Online 报表」（cgreport）或「Online 表单」（cgform）。

## 执行流程

读完本文件后直接 Write JSON 配置 → 执行 CLI 命令 → 输出预览链接。**两步完成，禁止多余动作。**

| 禁止 | 替代 |
|------|------|
| 读 .py 源码 | CLI 接受 JSON 配置，不用写 Python |
| 找 DB 凭证 | 用 memory 中的配置或问用户 |
| `python -c "..."` | **永远 Write .py 文件后 `python /path/to/file.py`**，`python -c` 会被放到后台导致超时 |
| 调外部 API 验证字段 | 直接按用户提供的字段写脚本，不预调 API |

## 前置条件

用户须提供 **API 地址** 和 **X-Access-Token**。SQL 数据集还需确认数据源（默认留空用服务自带数据源）。

## 🚀 CLI 创建（一条命令）

```bash
python /scripts/jimureport_creator.py \
  --api-base http://BASE_URL --token TOKEN --config /path/to/config.json
```

### 配置 A：SQL 普通/分组报表

```json
{
  "action": "create", "reportName": "报表名称", "theme": "blue",
  "datasets": [{"dbCode":"ds1","dbChName":"数据集","dbDynSql":"SELECT col1,col2 FROM t ORDER BY col1","dbSource":"","isPage":"0"}],
  "table": {"datasetCode":"ds1","title":"报表名称","columns":[
    {"field":"col1","title":"列1","width":120,"group":true},
    {"field":"col2","title":"列2","width":100,"funcname":"SUM"}
  ]}
}
```
> columns 可选属性：`group:true`(分组) / `funcname:"SUM"`(聚合) / `subtotalText:"小计"`

### 配置 B：SQL + 图表

```json
{
  "action":"create","reportName":"名称","layout":"chart_bottom",
  "datasets":[
    {"dbCode":"dt","dbChName":"表格","dbDynSql":"SELECT ...","isPage":"1"},
    {"dbCode":"dc","dbChName":"图表","dbDynSql":"SELECT x AS name,y AS value,'' AS type FROM ...","isPage":"0"}
  ],
  "table":{"datasetCode":"dt","title":"名称","columns":[...]},
  "chart":{"datasetCode":"dc","chartType":"bar.simple","title":"图表","width":"650","height":"380"}
}
```
> layout: `chart_bottom` / `chart_top` / `chart_right` / `chart_only`

### 配置 C：JSON 数据集（dbCode 必须字符串！）

```json
{
  "action":"create","reportName":"名称",
  "datasets":[{"dbCode":"my_data","dbChName":"数据","dbType":"3","isList":"1","isPage":"0",
    "jsonData":[{"name":"张三","age":"25"}],
    "fieldList":[["name","姓名"],["age","年龄"]]}],
  "table":{"datasetCode":"my_data","title":"名称","columns":[
    {"field":"name","title":"姓名","width":100},{"field":"age","title":"年龄","width":80}]}
}
```
> **禁止纯数字 dbCode**（如 gen_code()），JSON 数据集模板引擎无法解析。

### 配置 D：自定义 rows（复杂多级表头）

build_table_rows 无法满足时（如四级合并表头），传 `customRows` + `customMerges` 跳过自动构建：

```json
{
  "action":"create","reportName":"名称",
  "datasets":[{"dbCode":"ds1","dbType":"3","jsonData":[...],"fieldList":[...]}],
  "table":{"datasetCode":"ds1","columns":[{"field":"f1","title":"F1","width":100}]},
  "groupField":"ds1.group_field",
  "customRows":{"1":{"cells":{"1":{"text":"标题","style":0,"merge":[0,5]}},"height":40}},
  "customMerges":["B2:G2"],
  "customStyles":[{"align":"center","font":{"size":16,"bold":true}},{"align":"center","font":{"bold":true,"color":"#FFF"},"bgcolor":"#4472C4"},{"align":"center","valign":"middle"}],
  "customCols":{"0":{"width":27},"1":{"width":100},"len":100}
}
```

## 修改已有报表

```python
# get_report → 改 design → base_save（显式传 rows/cols/styles/merges/chartList，禁止 **design 展开）
designer, design = get_report(session, report_id)
design["rows"]["3"]["cells"]["1"]["text"] = "新值"
session.request("/save", base_save(report_id, designer,
    rows=design["rows"], cols=design["cols"], styles=design["styles"],
    merges=design["merges"], chartList=design.get("chartList", []),
    dbexps=design.get("dbexps", []),          # ← 不要漏掉，否则 DBSUM 失效
    isGroup=design.get("isGroup", False), groupField=design.get("groupField", ""),
))
```

## 报表类型判断

| 用户描述 | 数据绑定 | 数据集配置 |
|---------|---------|-----------|
| 明细/列表 | `#{db.field}` | isList:"1" isPage:"1" |
| 套打/单条 | `${db.field}` | isList:"0" isPage:"0" |
| 按XX分组 | `#{db.group(field)}` | isPage:"0" |
| 交叉表 | `#{db.groupRight(field)}` + `#{db.dynamic(field)}` | isPage:"0" |

## 行列索引规则

- 全部 0-indexed，A列(col0)留空，数据从 col1(B列)开始
- merge: `[extraRows, extraCols]`，0=只占自身
- merges 用 Excel 记法：`"B2:F2"`（UI行号 = code行号+1）

## 分组汇总

| 用户说法 | 实现 |
|---------|------|
| "合计行" | 数据行下方加 `=SUM(列号)` |
| "分组小计" | subtotal:"groupField" + funcname:"SUM" + subtotalText:"小计" |
| 只说"分组" | 只用 group() + aggregate:"group" |

## 查询参数（paramList）配置规范

### SQL 条件表达式

```sql
SELECT ... FROM t WHERE 1=1
<#if isNotEmpty(emp_name)> AND emp_name LIKE CONCAT('%','${emp_name}','%')</#if>
<#if isNotEmpty(hire_date_begin)> AND hire_date >= '${hire_date_begin}'</#if>
<#if isNotEmpty(hire_date_end)> AND hire_date <= '${hire_date_end}'</#if>
```

- `isNotEmpty(x)` — JimuReport 自定义函数，null 和 `""` 均返回 false（**必须用此函数，不能用 `?has_content` 或 `??`**）
- `${param}` — 用户查询参数；`#{sysUserCode}` — 系统变量，两者不可混用
- 解析字段时用不含 FreeMarker 的纯 SQL（`LIMIT 1`），避免解析失败

### paramList 字段值对照

| 控件 | widgetType | searchMode | searchFormat | dictCode |
|------|-----------|-----------|--------------|---------|
| 文本输入框 | `"String"` | `1` | `""` | 空 |
| 模糊查询输入框 | `"String"` | `5` | `""` | 空 |
| 日期选择 | `"date"` | `1` | `"yyyy-MM-dd"` | 空 |
| 日期时间 | `"date"` | `1` | `"yyyy-MM-dd HH:mm:ss"` | 空 |
| 年月 | `"date"` | `1` | `"yyyy-MM"` | 空 |
| 日期范围 | `"date"` | `2` | `"yyyy-MM-dd"` | 空 |
| **下拉单选** | `"String"` | **`4`** | `""` | 字典编码/SQL/API |
| **下拉多选** | `"String"` | **`3`** | `""` | 字典编码/SQL/API |

> **注意：参数不支持范围查询和模糊查询。**
> 日期范围须拆成两个独立参数（`_begin` / `_end`）；模糊匹配在 SQL 中手写 `LIKE '%${x}%'`。


## 默认样式规范

**所有报表 styles 必须带 border，不需要用户提醒。**

```python
# 方式1：直接用内置函数（推荐，自带边框）
from jimureport_utils import make_styles
styles = make_styles()  # 默认边框色 #d8d8d8

# 方式2：自定义颜色时手写，border 必须出现在每个 style dict 中
bd = {"bottom":["thin","#d8d8d8"],"top":["thin","#d8d8d8"],"left":["thin","#d8d8d8"],"right":["thin","#d8d8d8"]}
styles = [
    {**bd, "align":"center","valign":"middle","bgcolor":"#1F3864","color":"#ffffff","font":{"bold":True,"size":14}},  # 标题
    {**bd, "align":"center","valign":"middle","bgcolor":"#2F5496","color":"#ffffff"},  # 表头
    {**bd, "align":"center","valign":"middle"},   # 数据
    {**bd, "align":"right",  "valign":"middle"},  # 数字右对齐
]
```

> 参考报表有自己的 styles 时照搬，不要丢掉其中的 border 字段。

## 执行速度规范（3分钟内完成）

文件读取按场景取最小集：

| 场景 | 读取文件 |
|------|---------|
| 普通表格 / 分组 / JSON数据集 | **零文件预读，直接写脚本** |
| 含条码/二维码 | 只读 `references/cell-config.md` |
| 含图表 | 只读 `references/chart-echarts-templates.md` |
| 含表达式 | 只读 `references/expressions.md` |
| 有参考报表 ID | `get_report` 照搬，跳过所有文件 |

> `pitfalls.md` 常见坑已熟记，不需要每次都读。

## 已知坑点（必读）

> **写脚本前先 Read `references/pitfalls.md`**，避免踩坑重试浪费时间。
> **写循环块报表前必须先 Read `references/loopblock-grouping.md`**，里面有完整配置模板，禁止从头自己写。

## 工具脚本（按需使用）

| 操作 | 命令 |
|------|------|
| 查询报表 | `python report_tools.py --base-url URL --token T list [-k 关键词]` |
| 报表详情 | `python report_tools.py --base-url URL --token T detail <id>` |
| 删除/复制 | `python report_tools.py --base-url URL --token T delete/copy <id>` |
| 分享 | `python report_export.py share --name 名称` |
| 导出 | `python report_export.py export <id> --format pdf` |
| 改图表类型 | `python chart_tools.py change-type <id> bar.multi` |

> 冻结/rpbar/钻取联动/searchMode/完整参考文档索引 → 详见 `references/quick-ref.md`
> `references/chart-echarts-templates.md`（含图表时）
> 交叉报表 → `examples/multi-level-header.md`
> 钻取/联动 → `examples/report-drilling.md` / `examples/chart-linkage.md`
