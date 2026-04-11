# Online表单 / 设计器表单 生成图表技术指南

> 源码分析自 `packages/dragEngine/otherStyles/DragEngineScreen.vue` 及相关文件
> 适用于大屏（bigscreen）和仪表盘（dashboard）

---

## 一、概述

大屏"自定义"分类下有两种特殊组件类型：
- `compType: 'online'` → **Online表单**（基于 cgform）
- `compType: 'design'` → **设计器表单**（基于 desform）

这两类组件不走普通数据集流程，而是直接绑定表单数据，通过配置字段映射生成图表。
其标志性特征：`config.dataType = 4`。

---

## 二、完整流程（前端交互）

```
用户拖拽 online/design 到画布
  ↓
addPageComp() 检测到 ['online','design'].includes(item.compType)
  ↓
formType.value = item.compType        ← 记录是哪种表单类型
onlineRef.value.showModal()           ← 打开 FormSelectModal
  ↓
FormSelectModal：用户选择表单
  online: GET /online/cgform/head/list
  design: GET /desform/api/list/options
  确认后 emit('ok', { label, value, key, tableName, type, appId, appType })
  ↓
selectedOk(formObj) → showChartSetModal(formObj)
  ↓
ChartSetModal.showModal('add', formObj)
  formObj 赋值，调用 loadField() 加载字段
  ↓
loadField()
  online: GET /online/cgform/field/listByHeadId?headId={formObj.key}
  design: GET /desform/api/fields/{formObj.tableName}?subTable=true
  字段映射到 allFields（见下方字段结构）
  ↓
用户拖拽字段 → nameFields / valueFields / typeFields
用户选择图表类型（JBar/JPie/...）
  ↓
handleOk()：构建 saveData.config（见下方 config 结构）
emit('add', saveData)
  ↓
chartAdd(chartConfig)：newItem 加入 componentData
  component = chartConfig.component（如 'JBar'）
  config.dataType = 4
  config.formType = 'online'|'design'
```

---

## 三、字段结构

### Online 表单字段（来自 /online/cgform/field/listByHeadId）

过滤规则：`dbIsKey == 0 && dbIsPersist != 0`（非主键、已持久化）

```js
{
  fieldName: item.dbFieldName,      // DB字段名（API查询key）
  fieldTxt: item.dbFieldTxt,        // 显示名称
  fieldType: item.dbType,           // 'String'|'int'|'double'|'Date'|'Datetime'
  widgetType: item.fieldShowType,   // 控件类型：'text'|'date'|'sel'|'link_table'|...
  dictCode: item.dictField,         // 字典 code（用于翻译）
  dictField: ...,                   // 特殊：sel_user/sel_depart 时等于 dbFieldName
  dictTable: item.dictTable,
  dictText: item.dictText,
  fieldExtendJson: item.fieldExtendJson,
  // switch 控件特有
  switchOptions: ['Y', 'N'],
}
```

始终在 allFields 头部插入 `record_count`（记录数量）字段。

### 设计器表单字段（来自 /desform/api/fields/{code}?subTable=true）

过滤规则（排除以下类型）：
- `file-upload`、`imgupload`
- `options.type == 'dates'|'daterange'|'datetimerange'`

```js
{
  fieldName: item.model,            // 字段 code
  fieldTxt: item.name,              // 显示名称
  fieldType: 'string'|'number'|'date', // 归一化类型
  widgetType: item.type,            // 控件类型
  options: item.options,
  fieldShow: true,                  // false 时被过滤掉
  // 日期字段额外属性
  format: item.options.format,
  customDateType: '3',
  // 省市区级联
  customType: 'china',
}
```

特殊控件映射：
- `link-record`：fieldName = `item.options.titleField`，localField = item.model
- `sub-table-design`：fieldName = `item.children[0].model`，sourceCode = item.model
- 数值类控件（money/integer/number/rate/slider/formula/summary）→ fieldType = 'number'

始终在头部插入 `record_count`，并追加 `publicFields`（create_time 等公共字段）。

---

## 四、完整 Config 结构（dataType: 4）

```js
config: {
  // ===== 核心标记 =====
  dataType: 4,                      // 必须是 4，标识为表单图表
  formType: 'online'|'design',      // 表单类型

  // ===== 表单信息 =====
  formId: string,                   // online: cgform head ID; design: desform code
  formName: string,                 // 表单显示名称
  tableName: string,                // online: 实际表名; design: desform code（同 formId）
  type: undefined|'design'|'aggregation', // online 无此字段，design 为 'design'
  appId: string,                    // 所属应用 ID
  appType: 'current'|'other',       // 当前应用 or 其他应用

  // ===== 字段映射 =====
  nameFields: [                     // 维度字段（X轴/分类）
    { fieldName, fieldTxt, fieldType, widgetType, ... }
  ],
  valueFields: [                    // 数值字段（Y轴/指标）
    { fieldName, fieldTxt, fieldType, widgetType, ... }
  ],
  typeFields: [                     // 分组字段（仅分组图表）
    { fieldName, fieldTxt, fieldType, widgetType, ... }
  ],
  assistYFields: [],                // 辅助Y轴字段（双轴图）
  assistTypeFields: [],
  calcFields: [],                   // 计算字段（设计器表单特有）

  // ===== 时间过滤 =====
  sorts: { name: '' },
  filter: {
    queryField: 'create_time',
    queryRange: 'all',              // 'all'|'today'|'last7days'|'last30days'|...
  },

  // ===== 图表外观 =====
  chart: {
    category: 'Bar',                // 图表大类
    subclass: 'JBar',               // 图表组件名
    isGroup: false,
  },
  compStyleConfig: {},              // 样式配置
  analysis: {},                     // 分析配置
  filterField: [],                  // 筛选条件字段
  option: {},                       // ECharts option（基础）

  // ===== 其他 =====
  size: { height: 500 },
  turnConfig: { url: '' },
  jsConfig: '',
  drillData: [],
  authFieldShowResult: [],
  timeOut: 0,
}
```

---

## 五、运行时数据查询

当图表渲染时检测到 `config.dataType == 4`，调用：

```
POST /drag/onlDragDatasetHead/getTotalDataByCompId
```

请求体：
```js
{
  tableName: config.tableName,
  compName: component,              // 'JBar'|'JPie'|...
  config: {
    type: config.typeFields,
    name: config.nameFields,
    value: config.valueFields,
    assistValue: config.assistYFields,
    assistType: config.assistTypeFields,
    formType: config.formType,      // 'online'|'design'
    isAggregation: config.type === 'aggregation',
  },
  condition: {
    ...queryParams,                 // 时间范围、排序、联动参数等
  },
}
```

---

## 六、通过 API 创建设计器表单图表（正确步骤）

> **重要**：必须按照以下步骤创建，否则会出现以下错误：
> - `Cannot read properties of undefined (reading 'showTotal')` → compStyleConfig.summary 未定义
> - 设计弹窗打不开 → 字段配置不完整

### Step 1：查询设计器表单的字段结构

```python
# 获取表单字段 - 使用表单 code（不是表单 ID）
FORM_CODE = "ce_shi_yi_jian"  # 表单 code
resp = bi_utils._request('GET', f'/desform/api/fields/{FORM_CODE}', params={'subTable': True})
fields = resp.get('result', {}).get('fields', [])
# 解析字段：name 字段用 input 类型，value 字段用 number 类型
```

### Step 2：构建完整的 config（必须包含所有必需字段）

```python
cfg = {
    # ===== 核心标记 =====
    'dataType': 4,                      # 必须是 4
    'formType': 'design',                # 'online' 或 'design'

    # ===== 表单信息 =====
    'formId': FORM_CODE,               # 表单 code
    'formName': '测试意见',            # 表单显示名称
    'tableName': FORM_CODE,            # 表单 code
    'type': 'design',                   # design 表单固定值

    # ===== 字段映射 =====
    'nameFields': [                 # 维度字段
        {'fieldName': 'name', 'fieldTxt': '名称', 'fieldType': 'string', 'widgetType': 'input'}
    ],
    'valueFields': [                # 数值字段
        {'fieldName': 'number_xxx', 'fieldTxt': '数量', 'fieldType': 'number', 'widgetType': 'number'}
    ],
    'typeFields': [],              # 分组字段
    'assistYFields': [],
    'calcFields': [],

    # ===== 时间过滤 =====
    'sorts': {'name': ''},
    'filter': {'queryField': '', 'queryRange': 'all'},

    # ===== 图表配置 =====
    'chart': {
        'category': 'Funnel',       # 图表大类
        'subclass': 'JFunnel',     # 组件名
        'isGroup': False,
    },
    # ===== 样式配置（重要！必须包含 summary）=====
    'compStyleConfig': {
        'summary': {'showTotal': False, 'showY': False, 'decimals': 0}
    },
    'analysis': {},
    'filterField': [],
    'option': {'title': {'text': '漏斗图', 'show': True}},

    # ===== 其他 =====
    'size': {'height': 350},
    'turnConfig': {'url': '', 'type': '_blank'},
    'jsConfig': '',
    'drillData': [],
    'authFieldShowResult': [],
    'timeOut': 0,
}
```

### Step 3：添加组件

```python
comp = bi_utils.add_component(PAGE_ID, 'JFunnel', '漏斗图-设计器表单', x, y, w, h, cfg)
bi_utils.save_page(PAGE_ID)
```

### 常见错误汇总

| 错误信息 | 原因 | 解决方法 |
|---------|------|--------|
| `Cannot read properties of undefined (reading 'showTotal')` | `compStyleConfig.summary` 未定义 | 添加 `compStyleConfig: {'summary': {'showTotal': False}}` |
| `Cannot read properties of undefined (reading 'forEach')` | 字段配置不完整 | 确保 `nameFields` 和 `valueFields` 已正确设置 |
| 设计弹窗打不开 | config 结构不完整 | 参考 Step 2 的完整 config 结构 |
| 图表不渲染 | fieldName 错误 | 使用正确的字段名（从 `/desform/api/fields/{code}` 获取） |

返回数据后处理：
- `formType == 'design'`：调用 `handleCalcFields` + `handleTranslate`
- `formType == 'online'`：调用 `handleOnlineTranslateDict` + `handleTranslateDate` + `formatTimestamp`

---

## 六、设计模式数据查询（ChartSetModal 预览）

| 模式 | API |
|------|-----|
| JeecgBoot 积木BI设计页面 | `POST /drag/onlDragDatasetHead/getDataForDesign` |
| QQYun 预览 | `POST /drag/onlDragDatasetHead/getTotalData` |
| 渲染/播放模式（通用） | `POST /drag/onlDragDatasetHead/getTotalDataByCompId` |

---

## 七、涉及的全部 API 接口

| 用途 | 方法 | 路径 |
|------|------|------|
| 查询 Online 表单列表 | GET | `/online/cgform/head/list?keyword=&pageNo=1&pageSize=10&copyType=0` |
| 查询 Online 表单字段 | GET | `/online/cgform/field/listByHeadId?headId={id}` |
| 查询设计器表单列表 | GET | `/desform/api/list/options?keywords=&pageNo=1&pageSize=10` |
| 查询设计器表单字段 | GET | `/desform/api/fields/{code}?subTable=true` |
| 查询聚合表列表 | GET | `/drag/onlDragTableRelation/list?aggregationName=&pageSize=10` |
| 查询聚合表字段 | GET | `/drag/onlDragTableRelation/getFields/{code}` |
| 预览数据（积木BI） | POST | `/drag/onlDragDatasetHead/getDataForDesign` |
| 预览数据（QQYun） | POST | `/drag/onlDragDatasetHead/getTotalData` |
| 运行时数据查询 | POST | `/drag/onlDragDatasetHead/getTotalDataByCompId` |

---

## 八、API 自动创建图表（脚本化方案）

通过 API 直接创建 online/design 表单图表，无需前端交互：

### 步骤 1：查询表单信息
```python
# Online 表单
res = get('/online/cgform/head/list', {'keyword': '表单名', 'pageNo': 1, 'pageSize': 10, 'copyType': 0})
form = res['result']['records'][0]
form_id = form['id']
table_name = form['tableName']
form_name = form['tableTxt']

# 设计器表单
res = get('/desform/api/list/options', {'keywords': '表单名', 'pageNo': 1, 'pageSize': 10})
form = res['result'][0]
form_id = form['value']     # desform code
table_name = form['value']  # 同 form_id
form_name = form['label']
```

### 步骤 2：查询字段
```python
# Online 表单字段
res = get('/online/cgform/field/listByHeadId', {'headId': form_id})
fields = [f for f in res['result'] if f['dbIsKey'] == 0 and f['dbIsPersist'] != 0]
# 每个字段: dbFieldName, dbFieldTxt, dbType, fieldShowType, dictField

# 设计器表单字段
res = get(f'/desform/api/fields/{form_id}', {'subTable': 'true'})
fields = res['result']['fields']
# 每个字段: model(code), name(txt), type(widget), options
```

### 步骤 3：构建 config 并添加组件

> **⚠️ 两个必填字段（缺一不可，否则图表无法渲染且编辑弹窗报错）：**
> - `compStyleConfig` 必须包含完整 `summary` 子对象（`useEChartsNew.ts:396` 直接访问 `.summary.showTotal`，无 optional chaining，空 `{}` 会导致 `Cannot read properties of undefined (reading 'showTotal')`）
> - `filter` 必须包含 `conditionFields: []`（`ChartSetModal.initCompConfig` 调用 `dateConditionFormat(config.filter.conditionFields)`，该函数直接 `.forEach`，传 `undefined` 导致 `Cannot read properties of undefined (reading 'forEach')`）

```python
def make_form_chart_config(form_type, form_id, form_name, table_name,
                            name_fields, value_fields, chart_type='JBar',
                            chart_category='Bar', type_fields=None):
    """构建 dataType=4 的表单图表配置（经验证可渲染+可编辑的完整结构）"""
    def field_obj(f):
        """将原始字段转为 nameFields/valueFields 格式"""
        if form_type == 'online':
            return {
                'fieldName': f['dbFieldName'],
                'fieldTxt': f['dbFieldTxt'],
                'fieldType': f['dbType'],
                'widgetType': f.get('fieldShowType', 'text'),
                'dictCode': f.get('dictField', ''),
            }
        else:  # design
            ftype = 'number' if f['type'] in ['money','integer','number','rate','slider','formula','summary'] else 'string'
            if f['type'] == 'date': ftype = 'date'
            return {
                'fieldName': f['model'],
                'fieldTxt': f['name'],
                'fieldType': ftype,
                'widgetType': f['type'],
                'options': f.get('options', {}),
            }

    return {
        # === 核心标记 ===
        'dataType': 4,
        'formType': form_type,
        'formId': form_id,
        'formName': form_name,
        'tableName': table_name,
        'type': 'design' if form_type == 'design' else None,
        'appId': '',
        'appType': 'current',

        # === 字段映射 ===
        'nameFields': [field_obj(f) for f in name_fields],
        'valueFields': [field_obj(f) for f in value_fields],
        'typeFields': [field_obj(f) for f in (type_fields or [])],
        'assistYFields': [],
        'assistTypeFields': [],
        'calcFields': [],

        # === 排序（type 字段必须存在） ===
        'sorts': {'name': '', 'type': ''},

        # ⚠️ 必须含 conditionFields:[]，否则 dateConditionFormat(undefined) 报 forEach 错误
        # ⚠️ 必须含 customTime:[]，否则 initCompConfig 读取 undefined 报错
        'filter': {
            'queryField': 'create_time',
            'queryRange': 'all',
            'conditionMode': 'AND',
            'conditionFields': [],
            'customTime': [],       # ⚠️ 与手工配置的差异点：手工配置有此字段
        },

        # === 图表类型 ===
        'chart': {'category': chart_category, 'subclass': chart_type, 'isGroup': False},

        # ⚠️ 必须含完整 summary 子对象，否则 useEChartsNew.ts:396 报 showTotal 错误
        'compStyleConfig': {
            'summary': {
                'showY': True,
                'showTotal': False,
                'showField': 'all',
                'totalType': 'sum',
                'showName': '总计',
            },
            'showUnit': {
                'numberLevel': '',
                'decimal': None,
                'position': 'suffix',
                'unit': '',
            },
            'assist': {
                'summary': {'showY': True, 'showField': 'all', 'totalType': 'sum', 'showName': '总计'},
                'showUnit': {'numberLevel': '', 'decimal': None, 'position': 'suffix', 'unit': ''},
            },
            'headerFreeze': False,
            'unilineShow': False,
            'izPage': False,
            'columnFreeze': False,
            'lineFreeze': False,
            'showProgressText': True,
            'progress': {'show': True, 'name': '进度'},
            'target': {'show': True, 'name': '目标'},
        },

        # === 分析（字段需完整，否则 initCompConfig 设置 undefined 属性） ===
        'analysis': {
            'isRawData': True,
            'showMode': 1,
            'showData': 1,
            'showFields': [],
            'isCompare': False,
            'compareType': '',
            'trendType': '1',
            'compareValue': None,
            'izTimeOut': False,
            'timeOut': 0,
        },

        # === 其他（与手工配置的差异点）===
        'filterField': [],        # 手工配置有44个字段；初始可为空，ChartSetModal打开时自动填充
        'actionConfig': {'operateType': 'modal', 'modalName': '', 'url': ''},  # ⚠️ 手工配置有此字段
        'dataNum': '',           # ⚠️ 手工配置有此字段
        # ⚠️ option 字段必须有完整 ECharts 配置，不能为 {} 空对象
        # 手工配置的 option 包含：yAxis/xAxis/grid/series/tooltip/title/card 等
        # 这些配置由 ChartSetModal 打开后用户保存时从组件的 option 面板中提取并保存
        # skill 创建时需要预设与图表类型匹配的默认 option，否则图表渲染异常
        'option': _get_default_chart_option(chart_type),  # ⚠️ 必须有值
        'size': {'height': 500},
        'turnConfig': {'url': ''},
        'jsConfig': '',
        'drillData': [],
        'authFieldShowResult': [],
        'timeOut': 0,
        'background': '#FFFFFF00',
        'borderColor': '#FFFFFF00',
    }


def _get_default_chart_option(chart_type):
    """获取图表类型的默认 ECharts option 配置"""
    base_option = {
        'yAxis': {
            'axisLabel': {'color': '#EEF1FA'},
            'splitLine': {'lineStyle': {'color': '#8F8D8D'}, 'show': False, 'interval': 2},
            'yUnit': ''
        },
        'xAxis': {
            'axisLabel': {'color': '#EEF1FA'}
        },
        'grid': {
            'top': 43, 'left': 0, 'bottom': 18, 'right': 40, 'containLabel': True
        },
        'series': [],
        'tooltip': {
            'axisPointer': {'label': {'backgroundColor': '#333', 'show': True}, 'type': 'shadow'},
            'trigger': 'axis',
            'textStyle': {'color': '#EEF1FA'}
        },
        'title': {
            'textAlign': 'left', 'show': True, 'text': '',
            'textStyle': {'fontWeight': 'normal'}
        },
        'card': {
            'rightHref': '', 'size': 'default', 'extra': '', 'title': ''
        }
    }
    # 根据图表类型调整默认配置
    if chart_type == 'JStackBar':
        base_option['tooltip']['trigger'] = 'axis'
        base_option['series'] = [{'type': 'bar', 'barWidth': 'auto'}]
    elif chart_type == 'JPie':
        base_option.pop('yAxis', None)
        base_option.pop('xAxis', None)
        base_option['tooltip'] = {'trigger': 'item', 'textStyle': {'color': '#EEF1FA'}}
    elif chart_type == 'JLine':
        base_option['series'] = [{'type': 'line', 'smooth': False}]
    elif chart_type == 'JArea':
        base_option['series'] = [{'type': 'line', 'areaStyle': {}, 'smooth': False}]
    return base_option

# 构建 newItem 并 unshift 到 template
import uuid
COMP_W, COMP_H = 600, 450
new_item = {
    'componentName': f'{form_name}-柱形图',
    'component': 'JBar',
    'config': make_form_chart_config(...),
    'i': uuid.uuid4().hex,
    'x': 50, 'y': 100, 'w': COMP_W, 'h': COMP_H,
    'visible': True,
    'orderNum': 100,
    # 顶层字段（与 config 内部同步，防止组件初始不渲染）
    'size': {'width': COMP_W, 'height': COMP_H},
    'chart': {'category': 'Bar', 'subclass': 'JBar'},
    'turnConfig': {'url': ''},
    'linkageConfig': [],
}
# ⚠️ 正确保存方式：必须赋值 _page_components 再调 save_page，不能传 template 参数
bi_utils._page_components[page_id] = template
bi_utils.save_page(page_id)
```

---

## 九、关键差异对比

| 特性 | Online 表单（cgform） | 设计器表单（desform） |
|------|----------------------|-----------------------|
| 表单列表 API | `/online/cgform/head/list` | `/desform/api/list/options` |
| 字段 API | `/online/cgform/field/listByHeadId` | `/desform/api/fields/{code}?subTable=true` |
| tableName | 实际数据库表名 | desform code（= formId） |
| config.type | 无（undefined） | `'design'` |
| 计算字段 | 不支持 | 支持（calcFields） |
| 字典翻译 | handleOnlineTranslateDict | handleTranslate |
| 日期处理 | handleTranslateDate + formatTimestamp | handleCalcFields |
| 聚合表 | 不支持 | 支持（type='aggregation'） |
| 字段筛选 | dbIsKey==0 && dbIsPersist!=0 | 排除 file-upload/imgupload/date范围控件 |

---

## 十、compType 与最终 component 的关系

注意：`compType: 'online'|'design'` 只是触发表单选择弹窗的入口，
最终保存到 componentData 的 `component` 字段是用户在 ChartSetModal 中选择的图表类型（如 `JBar`、`JPie`、`JLine` 等）。

判断一个组件是否是表单图表：检查 `config.dataType == 4`，而非 `component` 字段。

编辑时（双击/右键编辑）：
```js
if (item.config.dataType == 4) {
  chartSetRef.value.showModal('edit', toRaw(item));
}
```

---

## 十一、使用技巧（AI 生成时参考）

### 11.1 何时选 Online 表单 vs 设计器表单

| 场景 | 推荐 |
|------|------|
| 通过 cgform 建的业务表（jeecg_demo 等） | **online** |
| 通过拖拽设计器（desform）建的表单 | **design** |
| 不确定时先调 `/online/cgform/head/list` 搜索，无结果再调 `/desform/api/list/options` | — |

### 11.2 字段角色分配建议

| 字段角色 | 放哪些字段 | 字段类型 |
|---------|-----------|---------|
| `nameFields`（X轴/维度） | 分类字段：部门、性别、状态、省份、产品名 | String/字符型 |
| `valueFields`（Y轴/指标） | 数值字段：金额、数量、评分；或 `record_count` | int/double/number/count |
| `typeFields`（分组/颜色区分） | 仅分组图表才用，选分类字段 | String |

**`record_count` 字段**（始终存在，放在 allFields 头部）：
- `fieldName: 'record_count'`，**`fieldType: 'count'`**（⚠️ 必须是 `'count'`，不能是 `'int'`/`'String'`）
- 用途：统计记录总数（不需要实际字段，后端生成 `COUNT(*)`）
- 最常用的 valueField，适合"统计各分类的数量"场景

> **⚠️ 高频踩坑（2026-04-09）**：将 `fieldType` 写成 `'int'` 会导致后端生成 `SUM(record_count)` → `SUM(*)` → SQL 语法错误。
> 正确定义：
> ```python
> {'fieldName': 'record_count', 'fieldTxt': '记录数量', 'fieldType': 'count', 'widgetType': 'count', 'dictCode': ''}
> ```

### 11.3 图表类型推荐

| 字段组合 | 推荐图表 | component |
|---------|---------|-----------|
| 1个nameField + 1个valueField（分类统计） | 饼图 | `JPie` |
| 1个nameField + 1个valueField（趋势/对比） | 柱形图 | `JBar` |
| 1个nameField + 多个valueField | 多系列柱形图 | `JMultipleBar` |
| 仅1个valueField（总量） | 数字图 | `JNumber` |
| 有typeField（分组颜色） | 分组柱形图 | `JMultipleBar` |
| 时间nameField + valueField（趋势） | 折线图 | `JLine` |
| 多nameField + 多valueField（交叉分析） | 透视表 | `JPivotTable` |

### 11.4 时间过滤配置

如果用户要求"近30天/本月/本年"等时间范围过滤，配置 `filter.queryRange`：

```python
'filter': {
    'queryField': 'create_time',   # 时间字段名（默认 create_time）
    'queryRange': 'last30days',    # all/today/yesterday/last7days/last30days/week/month/year
}
```

支持的 queryRange 值：
`all`（全部）、`today`、`yesterday`、`tomorrow`、`last7days`、`last30days`、
`week`（本周）、`preWeek`（上周）、`month`（本月）、`preMonth`（上月）、`year`（本年）

### 11.5 AI 创建 Online 表单图表的完整交互流程（强制）

> **用户说"使用 Online 表单创建图表"时，必须严格按以下三步执行，禁止自动猜测表单或字段。**

#### Step A：列出表单，询问用户选哪个

```python
# 查询表单列表（写入脚本文件执行，禁止 py -c 内联，因为 != 会被 shell 转义为 \!=）
res = bi_utils._request('GET', '/online/cgform/head/list',
    params={'keyword': '', 'pageNo': 1, 'pageSize': 20, 'copyType': 0})
records = (res.get('result') or {}).get('records') or []
for i, r in enumerate(records):
    print(f'[{i}] {r.get("tableTxt") or r["tableName"]} ({r["tableName"]})')
```

展示给用户：
```
找到以下 Online 表单，请问使用哪个？
  [0] 请假单 (oa_leave)
  [1] 员工信息 (demo)
  ...
```

#### Step B：查询所选表单字段，询问用户用哪些字段

```python
res2 = bi_utils._request('GET', '/online/cgform/field/listByHeadId', params={'headId': form_id})
fields = [f for f in (res2.get('result') or []) if f.get('dbIsKey') == 0 and f.get('dbIsPersist') != 0]
# 格式化展示字段供用户选择
for i, f in enumerate(fields):
    print(f'[{i}] {f["dbFieldName"]} ({f.get("dbFieldTxt","")}) - {f["dbType"]}')
```

展示给用户：
```
请选择字段：
  维度字段（饼图分类）：[4] leave_type(请假类型) / [15] sys_org_name(部门) / ...
  数值字段：record_count(记录数量) / [8] leave_days(请假天数) / ...
```

#### Step C：根据用户选择创建图表（写脚本文件执行）

**⚠️ 执行规范（强制）：**
1. **必须 Write 脚本到文件，禁止 `py -c "..."`** —— 因为 `!=` 在 shell 中被转义为 `\!=` 导致 SyntaxError
2. **`sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`** —— 用脚本自身所在目录，不能用 `.`（`.` 取决于 shell 启动目录，不可靠）
3. **`cp bi_utils.py` 目标必须用绝对路径** —— `"C:/Users/25067/bi_utils.py"`，不能用 `.`
4. **cp 和 Write 脚本并行** —— 同一轮工具调用，节省一轮

**正确执行模板（2轮）：**
```
轮次1（并行）: cp bi_utils.py "C:/Users/25067/bi_utils.py" && ls 验证  +  Write 脚本文件
轮次2: cd C:/Users/25067 && py 脚本.py && echo URL | clip.exe && rm 脚本.py bi_utils.py
```

### 11.6 脚本化创建完整示例（Online 表单 → 饼状图，经验证可用）

```python
import os, sys, json, uuid
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # ⚠️ 用脚本所在目录，不能用 '.'
import bi_utils

bi_utils.API_BASE = 'http://your-api.com'
bi_utils.TOKEN = 'your-token'
PAGE_ID = 'your-page-id'

# 1. 查询 Online 表单列表
res = bi_utils._request('GET', '/online/cgform/head/list',
    params={'keyword': '', 'pageNo': 1, 'pageSize': 20, 'copyType': 0})
records = (res.get('result') or {}).get('records') or []
form = records[0]   # 或按名称筛选
form_id    = form['id']
table_name = form['tableName']
form_name  = form.get('tableTxt') or form.get('tableName')

# 2. 查询字段（过滤非主键、已持久化）
res2 = bi_utils._request('GET', '/online/cgform/field/listByHeadId',
    params={'headId': form_id})
raw_fields = [f for f in (res2.get('result') or [])
              if f.get('dbIsKey') == 0 and f.get('dbIsPersist') != 0]

# 选分类字段（优先 sex/type/status/dept 等）
cat_fields = [f for f in raw_fields
              if f.get('dbType') == 'String'
              and f.get('fieldShowType') not in ('date','datetime','file','image','umeditor')]
pref_keys = ('sex','type','status','dept','category','grade')
name_field = next(
    (f for k in pref_keys for f in cat_fields if k in f['dbFieldName'].lower()),
    cat_fields[0] if cat_fields else raw_fields[0]
)

def field_obj_online(f):
    return {
        'fieldName': f['dbFieldName'],
        'fieldTxt':  f['dbFieldTxt'],
        'fieldType': f['dbType'],
        'widgetType': f.get('fieldShowType', 'text'),
        'dictCode':  f.get('dictField', ''),
    }

record_count_field = {
    'fieldName': 'record_count', 'fieldTxt': '记录数量',
    'fieldType': 'count', 'widgetType': 'text', 'dictCode': '',
}

# 3. 构建完整 config（必须包含 compStyleConfig.summary 和 filter.conditionFields）
config = {
    'dataType': 4,
    'formType': 'online',
    'formId': form_id,
    'formName': form_name,
    'tableName': table_name,
    'type': None,
    'appId': '', 'appType': 'current',
    'nameFields':  [field_obj_online(name_field)],
    'valueFields': [record_count_field],
    'typeFields': [], 'assistYFields': [], 'assistTypeFields': [], 'calcFields': [],
    'sorts': {'name': '', 'type': ''},
    # ⚠️ conditionFields 必须存在，否则 dateConditionFormat(undefined) 报 forEach 错误
    'filter': {
        'queryField': 'create_time', 'queryRange': 'all',
        'conditionMode': 'AND', 'conditionFields': [],
    },
    'chart': {'category': 'Pie', 'subclass': 'JPie', 'isGroup': False},
    # ⚠️ compStyleConfig.summary 必须完整，否则 useEChartsNew.ts:396 报 showTotal 错误
    'compStyleConfig': {
        'summary': {'showY': True, 'showTotal': False, 'showField': 'all', 'totalType': 'sum', 'showName': '总计'},
        'showUnit': {'numberLevel': '', 'decimal': None, 'position': 'suffix', 'unit': ''},
        'assist': {
            'summary': {'showY': True, 'showField': 'all', 'totalType': 'sum', 'showName': '总计'},
            'showUnit': {'numberLevel': '', 'decimal': None, 'position': 'suffix', 'unit': ''},
        },
        'headerFreeze': False, 'unilineShow': False, 'izPage': False,
        'columnFreeze': False, 'lineFreeze': False, 'showProgressText': True,
        'progress': {'show': True, 'name': '进度'}, 'target': {'show': True, 'name': '目标'},
    },
    'analysis': {
        'isRawData': True, 'showMode': 1, 'showData': 1, 'showFields': [],
        'isCompare': False, 'compareType': '', 'trendType': '1',
        'compareValue': None, 'izTimeOut': False, 'timeOut': 0,
    },
    'filterField': [], 'option': {}, 'size': {'height': 500},
    'turnConfig': {'url': ''}, 'jsConfig': '', 'drillData': [],
    'authFieldShowResult': [], 'timeOut': 0,
    'background': '#FFFFFF00', 'borderColor': '#FFFFFF00',
}

# 4. 读取页面，置顶插入新组件
page = bi_utils.query_page(PAGE_ID)
tmpl = page.get('template', [])
if isinstance(tmpl, str):
    try: tmpl = json.loads(tmpl)
    except: tmpl = []

COMP_W, COMP_H = 600, 450
new_comp = {
    'componentName': f'{form_name}-饼状图',
    'component': 'JPie',
    'config': config,
    'i': uuid.uuid4().hex,
    'x': 50, 'y': 100, 'w': COMP_W, 'h': COMP_H,
    'visible': True, 'orderNum': 100,
    'size': {'width': COMP_W, 'height': COMP_H},
    'chart': {'category': 'Pie', 'subclass': 'JPie'},
    'turnConfig': {'url': ''}, 'linkageConfig': [],
}
tmpl.insert(0, new_comp)
# ⚠️ 必须赋值 _page_components 再调 save_page（不能给 save_page 传 template 参数）
bi_utils._page_components[PAGE_ID] = tmpl
bi_utils.save_page(PAGE_ID)
print(f'创建成功！组件: {form_name}-饼状图')
```

### 11.7 常见问题与排错

| 问题 | 原因 | 解决 |
|------|------|------|
| 图表无数据 | nameFields/valueFields 为空 | 至少设置1个 valueField |
| 饼图无颜色区分 | 没有设置 nameField | nameField 设置分类字段 |
| 字典值未翻译（显示0/1而非男/女） | online 表单字段缺 dictCode | 检查 field.dictField 是否有值 |
| 设计器表单字段加载失败 | tableName 传的不是 desform code | design 模式的 tableName = formId = desform code |
| 运行时数据为空 | tableName 与表单不对应 | online 用 tableName，design 用 formCode |
| 图表不显示（大屏） | config 中 size.height 太小 | 设为 400~600 |
| **图表渲染报错 `Cannot read properties of undefined (reading 'showTotal')`** | `config.compStyleConfig` 是空对象 `{}`，`useEChartsNew.ts:396` 直接访问 `.summary.showTotal`（无 optional chaining） | `compStyleConfig` 必须包含完整 `summary` 子对象（见上方完整 config 模板） |
| **编辑弹窗报错 `Cannot read properties of undefined (reading 'forEach')`** | `config.filter` 缺少 `conditionFields` 字段，`ChartSetModal.initCompConfig` 调用 `dateConditionFormat(config.filter.conditionFields)`，该函数直接调 `condition.forEach`，传 `undefined` 崩溃 | `filter` 中必须加 `'conditionFields': []` |
| **`option: {}` 空对象导致图表渲染异常** | skill 创建时 `option` 为空对象 `{}`，而手工配置有完整 ECharts 配置（yAxis/xAxis/grid/series/tooltip等），图表组件依赖 `option` 中的结构进行渲染和数据绑定，`{}` 会导致图表无法正常渲染 | `option` 必须传入与图表类型匹配的完整 ECharts 配置，不能为空对象 |
| **`filter.customTime` 缺失** | `initCompConfig` 中读取 `config.filter.customTime`，若缺失则 `customTime && customTime.length > 1` 报空指针 | `filter` 中必须加 `'customTime': []` |
| **`save_page` 报错或覆盖页面** | 调用 `bi_utils.save_page(page_id, template)` 传了 template 参数（该参数不存在） | 必须用 `bi_utils._page_components[page_id] = tmpl` 赋值后再 `bi_utils.save_page(page_id)` |
| **`py -c "..."` 内联脚本 SyntaxError：`\!=`** | shell 把 `!=` 转义为 `\!=`，Python 解析报 `unexpected character after line continuation character` | **禁止用 `py -c`**，必须 Write 脚本到文件再 `py script.py` |
| **`ModuleNotFoundError: No module named 'bi_utils'`** | `sys.path.insert(0, '.')` 中的 `.` 解析为 shell 启动目录，不是脚本所在目录 | 脚本开头用 `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))` 动态获取脚本目录；且 `cp bi_utils.py` 目标必须与脚本文件在同一目录（绝对路径） |
| **设计器表单弹窗字段为空** | `config.formType` 未设置或值错误，前端调用 `/online/cgform/field/listByHeadId` 而非 `/desform/api/fields/{code}` | 必须设置 `formType: 'design'`（让前端调用设计器表单接口） |
| **设计器表单弹窗字段为空（进阶排查）** | `config.formId`/`tableName` 传了表单 ID（数值）而非表单 code（字符串） | design 模式的 `formId` 和 `tableName` 都必须传**表单 code**（如 `ru_ku_dan_nbc0`），不是表单 ID |
| **弹窗显示了字段，但未绑定到维度/数值栏位** | 缺少 `nameFields` 和 `valueFields` 配置，前端加载字段后用户手动拖拽但未保存 | 必须手动设置 `nameFields`（维度）和 `valueFields`（数值）数组，并保存到组件 config |

---

## 十二、设计器表单绑定字段的完整配置（2026-04-03 更新）

### 12.1 完整 config 结构

```python
cfg = {
    # === 核心标记 ===
    'dataType': 4,                      # 必须是 4
    'formType': 'design',               # 区分 Online/design 的关键字段

    # === 表单信息 ===
    'formId': form_code,                 # 设计器表单 code（如 'ru_ku_dan_nbc0'）
    'formName': form_name,              # 表单显示名称（如 '入库单'）
    'tableName': form_code,              # 同 formId
    'type': 'design',                    # design 表单固定值

    # === 字段映射（关键！没有这些字段，弹窗中字段不会绑定到维度/数值）===
    'nameFields': [                      # 维度字段（X轴/分类）
        {
            'fieldName': 'select_1763351325746_348911',  # 字段 model
            'fieldTxt': '入库类型',           # 显示名称
            'widgetType': 'select',        # 控件类型
        }
    ],
    'valueFields': [                     # 数值字段（Y轴/指标）
        {
            'fieldName': 'record_count', # 记录数量（COUNT）
            'fieldTxt': '记录数量',
            'widgetType': 'text',
            'fieldType': 'count'
        }
    ],
    'typeFields': [],                  # 分组字段（仅多系列图表）
    'assistYFields': [],                # 辅助Y轴

    # === 时间/筛选条件 ===
    'filter': {
        'queryField': '',
        'queryRange': 'all',
        'conditionFields': [],            # 必须有空数组
        'customTime': [],                # ⚠️ 必须有此字段
    },

    # === 图表配置 ===
    'chart': {
        'category': 'Funnel',
        'subclass': 'JFunnel',
    },

    # === 样式配置（必须有 summary！）===
    'compStyleConfig': {
        'summary': {'showTotal': True}
    },

    # === 其他（与手工配置的差异点）===
    'filterField': [],                   # 手工配置有44个字段；初始可为空
    'actionConfig': {'operateType': 'modal', 'modalName': '', 'url': ''},  # ⚠️ 手工配置有此字段
    'dataNum': '',                       # ⚠️ 手工配置有此字段
    'option': {},                        # ⚠️ 必须有完整 ECharts 配置，不能为空
}
```

### 12.2 正确流程（参考 online 表单流程）

1. **创建空组件**: `comp_ops.py add --comp JFunnel`
2. **查询设计器表单字段**: `GET /desform/api/fields/{form_code}?subTable=true`
3. **询问用户选择维度/数值字段**
4. **绑定配置**: 设置 `formType='design'`, `formId`, `tableName`, `type='design'`, `nameFields`, `valueFields`
5. **保存并验证**

### 12.3 前端字段区分（关键区分点）

| 判断条件 | 调用接口 |
|---------|---------|
| `config.formType == 'design'` | `GET /desform/api/fields/{tableName}?subTable=true` |
| `config.formType == 'online'` | `GET /online/cgform/field/listByHeadId?headId={formId}` |

前端弹窗逻辑（ChartSetModal.vue）：
- `type === 'design'` → 调用 `getDesignField(formObj.value.tableName)`
- `type === 'aggregation'` → 调用 `getAggregationFormField(formObj.value.tableName)`
