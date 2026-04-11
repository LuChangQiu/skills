# JSON数据集与单元格绑定

积木报表通过 API 创建 JSON 数据集，并将字段绑定到单元格的完整参考。

---

## 1. JSON数据集（dbType="3"）

### saveDb 关键字段

```python
{
    "izSharedSource": 0,
    "jimuReportId": report_id,
    "dbCode": "person",          # 数据集编码（绑定时用）
    "dbChName": "人员信息",       # 中文名称（设计器显示）
    "dbType": "3",               # JSON 数据集
    "dbSource": "",
    "isList": "0",               # "0"=对象数据集，"1"=列表数据集
    "isPage": "0",               # "0"=不分页（对象必须为"0"）
    "dbDynSql": "",              # JSON数据集留空
    "jsonData": json.dumps({     # 必须用 {"data":[...]} 包裹！
        "data": [{"xingming": "张三", "nianling": "25"}]
    }, ensure_ascii=False),
    "apiConvert": "",
    "fieldList": [...],
    "paramList": [],
}
```

> **重要：`jsonData` 必须用 `{"data": [...]}` 对象包裹，禁止直接传数组 `[...]`。**
> 直接传数组会导致预览报错：`offset 1, character [, line 1, column 1`

### 对象 vs 列表模式

| 模式 | isList | isPage | 绑定语法 | 适用场景 |
|------|--------|--------|---------|---------|
| 对象数据集 | `"0"` | `"0"` | `${dbCode.field}` | 套打、证件、单条记录 |
| 列表数据集 | `"1"` | `"1"`或`"0"` | `#{dbCode.field}` | 明细列表、统计报表 |

### fieldList 字段格式

```python
field_list = [
    {
        "fieldName": "xingming",    # 字段名（与 jsonData 中的 key 一致）
        "fieldText": "姓名",         # 中文标签（设计器显示）
        "widgetType": "String",     # 类型，一般用 String
        "orderNum": 0,              # 排序号，从 0 递增
        "tableIndex": 0,
        "extJson": "",
        "dictCode": "",
    },
    ...
]
```

---

## 2. 单元格填入数据集绑定

通过 `/jmreport/save` 的 `rows` 字段写入绑定表达式：

```python
rows = {
    "0": {                                         # 第1行（0-based）
        "cells": {
            "0": {"text": "姓名"},                 # A1 静态文本
            "1": {"text": "年龄"},                 # B1 静态文本
        }
    },
    "1": {                                         # 第2行
        "cells": {
            "0": {"text": "${person.xingming}"},   # A2 对象绑定
            "1": {"text": "${person.nianling}"},   # B2 对象绑定
        }
    },
}
```

**绑定语法：**
- 对象数据集：`${dbCode.fieldName}`（单值替换，不循环）
- 列表数据集：`#{dbCode.fieldName}`（循环展开多行）

---

## 3. 条件隐藏行/列

### 数据结构

```python
"hidden": {
    "rows": ["1:1"],                  # 登记要控制的行范围（0-based，起:止，闭区间）
    "cols": ["1:1"],                  # 登记要控制的列范围
    "conditions": {
        "rows": {
            "1:1": "person.xingming=='张三'"   # aviator 表达式
        },
        "cols": {
            "1:1": "person.xingming=='张三'"
        }
    }
}
```

> **关键约束：条件行/列必须同时登记到 `hidden.rows`/`hidden.cols` 中。**
> 只在 `conditions` 里加，不在 `rows`/`cols` 里登记，条件不会生效。

### 条件表达式（aviator 语法）

| 需求 | 表达式 |
|------|--------|
| 字段等于某值 | `"person.xingming=='张三'"` |
| 字段大于某值 | `"person.age>18"` |
| 字段不等于 | `"person.dept!='技术部'"` |
| 始终隐藏（等效静态隐藏） | `"1==1"` |
| 复合条件 AND | `"person.dept=='技术部'&&person.age>30"` |
| 复合条件 OR | `"person.dept=='技术部'||person.dept=='产品部'"` |

字段引用格式：`数据集编码.字段名`（与 saveDb 中的 `dbCode` 和 `fieldName` 一致）

### 设置条件隐藏

```python
hidden = sheet.get("hidden", {"rows": [], "cols": [], "conditions": {"rows": {}, "cols": {}}})
hidden.setdefault("conditions", {})
hidden["conditions"].setdefault("rows", {})
hidden["conditions"].setdefault("cols", {})

# 设置行条件
if "1:1" not in hidden["rows"]:
    hidden["rows"].append("1:1")
hidden["conditions"]["rows"]["1:1"] = "person.xingming=='张三'"

# 设置列条件（年龄列 B列 index=1）
if "1:1" not in hidden["cols"]:
    hidden["cols"].append("1:1")
hidden["conditions"]["cols"]["1:1"] = "person.xingming=='张三'"

sheet["hidden"] = hidden
```

### 取消条件隐藏

```python
# 取消行条件
hidden["rows"] = [r for r in hidden["rows"] if r != "1:1"]
hidden["conditions"]["rows"].pop("1:1", None)

# 取消列条件
hidden["cols"] = [c for c in hidden["cols"] if c != "1:1"]
hidden["conditions"]["cols"].pop("1:1", None)
```

---

## 4. 预览行为

- **条件隐藏行**：预览时满足条件的行整行消失，后续行索引上移
- **条件隐藏列**：预览时满足条件的列整列消失，后续列索引左移
- **静态隐藏行/列**（只在 `hidden.rows`/`hidden.cols` 中登记，不加 `conditions`）：始终隐藏

---

## 5. 实现方式

JSON 数据集创建和条件隐藏均通过 `jimureport_utils.py` 的 `save_db()` / `get_report()` / `base_save()` 直接在 heredoc 脚本中实现。
