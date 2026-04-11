# 已知坑点速查

遇到异常时先查此表。

| 坑 | 现象 | 解决 |
|----|------|------|
| dbCode 纯数字（所有数据集） | `#{1775721592817440.field}` 预览数据全空 | **所有类型数据集**（SQL/JSON/API）的 dbCode 均禁止纯数字；必须用字母开头的驼峰字符串如 `"schoolJf"`，禁止 `gen_code()` 直接作为 dbCode |
| dbCode 含保留关键词或特殊字符 | 数据集保存异常或绑定失败（如 `returnOrder` 含 `return`） | dbCode 只能用纯字母+数字的驼峰命名；**禁止含 `return`、`for`、`if`、`while` 等 JS/Java 保留字**；**禁止含下划线 `_`、连字符 `-`、点 `.` 等特殊字符**；正确示例：`thdMain`、`salesOrder`、`empInfo` |
| save 返回值取错路径 | `resp.get("id")` 返回 None，后续全部静默失败 | 正确路径：`resp["result"]["id"]` |
| 预览/设计器 URL 用 `?id=` | 页面可能加载但报表为空 | 正确格式：`/jmreport/view/{id}` 和 `/jmreport/index/{id}`（路径参数） |
| rows/cols 被 json.dumps | 设计器空白 | 只 dumps designerObj |
| gen_code() 同秒重复 | INSERT code 唯一键冲突 | 用毫秒+随机数：`str(time.time()*1000)+str(random.randint(100,999))`；多报表顺序创建时加 `time.sleep(2)` |
| save_db 之间加 sleep | 脚本慢 1~2 秒 | `save_db` 内部用 `gen_id()`（毫秒+随机），**不会重复**；同一报表的多个数据集之间**不需要 sleep**，直接顺序调用即可 |
| 只改报表展示配置也调 save_db | 多调了一次不必要的接口 | 修改 rpbar/样式/合并等**纯报表配置**时，不需要调 `save_db`；直接 `get_report` → 改配置 → `/save` 两步即可 |
| 修改数据集单个字段（如 isPage）用 save_db 全量重传 | 代码繁琐，需要重新填写所有参数 | 正确做法：`update_db(session, db_id, isPage="1")`；内部先 `/loadDbData/{dbId}` 取回原始数据，只改指定字段，原样回传 `/saveDb`（所有接口本身都很快，<0.1s）|
| 图表 linkIds 放顶层 | 钻取/联动无效 | 放 extData 内部 |
| 联动目标图表无默认值 | 初始页面图表空白 | paramList 必须设 paramValue |
| isPage:"1" + 分组 | 合并/合计不完整 | 分组报表数据集 isPage:"0" |
| bar.multi 用 apiStatus:"1" | 图表渲染异常 | 静态数据必须用 apiStatus:"0" |
| dbSource 传名称不传 ID | 数据源下拉不显示 | 先 getDataSourceByPage 查 ID |
| SQL 数据集 dbSource 留空 | 界面打开数据集看不出用的是哪个数据库/数据源 | SQL 数据集必须传 `dbSource` 数据源 ID（非空字符串）；从 memory 取或先调 getDataSourceByPage 查询 |
| executeSelectApi 调用方式 | POST + query string，不是 JSON body；result 直接是 fieldList 数组 | 用 `parse_api(session, url)` |
| 脚本走系统代理 | 连接失败 | Session 已封装 trust_env=False |
| paramValue 用图表字段名 | 图表钻取无值 | 用 name/value/seriesName |
| 诊断命令用 run_in_background | 用户等待输出超时 | 诊断/计时命令必须前台同步执行，禁止 run_in_background |
| 修改已有报表用 `**design` | design 含 `name` 等字段冲突，图表消失 | 始终显式传 `rows=design['rows'], cols=design['cols'], styles=..., merges=..., chartList=...`，禁止 `**design` |
| 图表 extData.id 为 None | 预览图表不渲染/消失 | `extData` 中 `chartId` 和 `id` 必须同时赋值为 `layer_id`，不可缺一 |
| 只改 `color[]` 设置颜色 | 颜色不生效或不持久化 | 饼图改3处(data[i].itemStyle/label/colors[])，柱形图改2处(series[i].itemStyle/colors[])，`color[]` 不动 |
| cell 直接写 `align`/`font`/`valign` | 样式不生效（浏览器实测 2026-04-07） | 对齐+字体必须放入顶层 `styles[]` 数组，cell 用 `style` 整数索引引用；不能把 align/font/valign 直接写在 cell 对象上 |
| `color`（文字颜色）写在 `font` 内 | `font.color` 在某些 style 不生效，表头白字不显示 | `color` 必须在 style 顶层，与 `font`/`bgcolor` 同级：`{"font":{...}, "color":"#FFFFFF", "bgcolor":"..."}` |
| `merge` 不加 `merges` 顶层数组 | 合并区域在设计器显示为未合并 | cell 设 `merge:[rowSpan,colSpan]` 同时，**必须**在顶层 `merges` 加 `"B1:J1"` 等 Excel 范围字符串（UI 行号 = code 行号+1） |
| `merge` 与顶层 `merges` 列范围不一致 | 单元格合并只到部分列，右侧留空白（如收货地址未对齐） | cell `merge:[0,N]` 表示额外跨 N 列，顶层 `merges` 的结束列必须一致：`merge:[0,4]` → 起始列为C时应为 `"C?:G?"` 而非 `"C?:E?"`；**改 merge 必须同步核查 merges 字符串** |
| 用切片限制图表数据条数 | SQL LIMIT 或 Python 切片控制不稳定 | 图表 config 中设 `"dataFilter":{"filterCount":N}`，积木报表引擎会自动只显示前 N 条；SQL 不加 LIMIT |
| 象形图 symbol 图片 URL 拼错 | 图标看不到 | upload 返回 `message="jimureport/x.png"`；访问 URL = `BASE_URL + "/img/" + message`；symbol 写 `f"image://{BASE_URL}/img/{message}"` |
| 象形图开启补全用 `symbolClip` | 补全不生效 | 补全（背景虚影）用 `"double": True`，不是 `symbolClip` |
| 雷达图 series 传空字符串 | 系列属性"请选择"，legend 显示 undefined | SQL 里 `'' AS type` 只是占位，`chart_entry(series="type")` 仍必须填 `"type"` |
| 雷达图 legend.data 为空数组 | 图例显示空白方块 | `legend.data` 必须预填系列名列表，如 `["综合评分"]`；SQL动态数据集引擎不会自动填充 legend.data |
| 雷达图 SQL type 字段传空字符串 | 图例空白、tooltip 显示 series0 | 引擎用 type 字段值作为系列名；必须传实际名称如 `'综合评分' AS type`，且与 `legend.data` 和 `series[].data[].name` 三处保持一致 |
| 同一报表多图表垂直排列重叠 | 第二个图表盖在第一个上 | chart_entry rowspan 默认14但 height=420px 实际占≈17行；第二个图表的 row 必须 ≥ 第一个 row + ceil(height/行高) + 间距，保守估算：height=420 时第二图表 row = 第一图表 row + 20 |
| 表达式列写 `=` 开头 | 后端将文本当公式求值，显示计算结果而非表达式字符串 | 表达式说明列（col2）去掉 `=` 前缀，只写 `ABS(-88.5)` 而非 `=ABS(-88.5)` |
| `CEIL(n)` / `FLOOR(n)` 无结果 | JimuReport 内置函数不含 CEIL/FLOOR，只有 Aviator 的 `math.ceil/floor` 有效 | 去掉这两行；若需要向上/向下取整只能用 `math.ceil()`/`math.floor()` |
| `UPPER(#{field})` / `LOWER(#{field})` 无结果 | `#{field}` 替换后变成 `UPPER(Hello World)`（无引号），Aviator 解析失败；且绑定字段的行会随数据集展开重复多行 | 改用字符串字面量：`=UPPER('hello world')`；不要在 UPPER/LOWER 公式内使用 `#{}` 绑定 |
| get_report→删行→shift 后按硬编码行号修改 | 行号计算出错，改错了行 | 删行/移行后，按 col1 函数名（文本内容）匹配目标行，而非依赖行号索引 |
| rpbar 用 json.dumps 字符串 | 保存成功但预览工具条设置不生效 | rpbar 必须用 dict 对象，不能用 `json.dumps()`；字段名是 `rpbar`（不是 rqbar） |
| 单系列图表 series 传了 `"type"` | 预览时图表不自动加载，需手动点击"运行"按钮 | 单系列图表（pie/bar.simple/line.simple 等）`series` 必须传空字符串 `""`；`"type"` 仅用于多系列图表（bar.multi 等）且数据集中确实有该字段时才传 |
| get_report 对新报表失败 | 刚 /save 创建的报表调 get_report 返回 None | 改为从 create 响应手动构建 designer dict |
| customRows 仍需 datasetCode | build_table_rows 报 KeyError | 即使用 customRows，table 里也必须有 `"datasetCode":""` 占位 |
| report_tools.py 参数名 | 命令行报错 unrecognized arguments | 用 `--base-url`，不是 `--api-base` |
| MySQL Docker 中文乱码 | 中文以 latin1 存储损坏 | 必须加 `--default-character-set=utf8mb4` |
| FreeMarker 空值判断 | 条件不生效 | 用 `isNotEmpty(x)` 而非 `x??` 或 `x?has_content`；后两者无法过滤空串 `""` |
| 文本参数 widgetType | 控件渲染异常 | 应为 `"string"`，不是 `"text"` |
| LIKE 模糊查询写法 | 必须用 `LIKE CONCAT('%','${x}','%')`，不能用 `LIKE '%${x}%'`；后者 `${x}` 展开为 JDBC 占位符后嵌在字符串字面量里无法绑定 |
| 下拉控件配置 | 下拉单选：`widgetType:"String"` + `searchMode:4`；下拉多选：`widgetType:"String"` + `searchMode:3`；`widgetType` 不能用 `"sel_search"`，否则控件渲染异常 |
| loopTime 标题列范围含尾部空白列 | 标题偏窄，右侧留白，与内容区不对齐 | loopTime 分栏时若循环块末尾有间距列（如 col4=20px），第2张卡片复制后产生 col9（尾部空白）；**标题行的 merge 和 merges 不应包含该列**。正确范围：A1:I1（col0-col8），内容区 col0-col3+col4间距+col5-col8 = 820px 对齐；col9（尾部空白）排除在外 |
| 分版用 loopBlockList | 并列多数据集表格数据错乱/联动 | 分版场景禁止用 loopBlockList；正确做法：第一个表无标记（`#{}` 自然展开），右侧表单元格加 `zonedEdition:N`，顶层加 `zonedEditionList`（结构同 loopBlockList，含 db 字段），loopBlockList 留空 `[]` |
| save_db 重复创建数据集 | 不传 `db_id` 时每次都 INSERT 新记录，多次运行后报表内出现多个同名数据集；**更新时必须传 `db_id=<已有ID>`** |
| save_db 返回值误用 | `save_db()` 直接返回数据集 ID 字符串，不是 dict；错误用 `r["result"]["id"]` 会 TypeError | 直接用 `db_id = save_db(...)` |
| 主子表循环块用两个 loopBlock | 以为要分别配主表和子表各一条 loopBlockList → 无效，子表不展开 | **只有一个 loopBlockList，db=主表**；子表行（`#{sub.field}`）嵌入同一循环块模板，引擎靠 link 关联自动展开 |
| loopBlockList eri 设太大 | eri=35/36 等很大值 → 子表记录少时预览页出现大片空白 | eri 设为**模板内容末行 + 2~3 行缓冲**即可；引擎自动按数据量扩展，数据多不截断，数据少不留白 |
| `/link/saveAndEdit` 参数格式错误 | 用 `mainDbId/subDbId/paramList` → 关联不生效，子表数据不展开 | 正确格式：`reportId` + `mainReport/subReport`（dbCode别名）+ `parameter`（JSON字符串含 main/sub/subReport 数组）+ `linkType:"4"` |
| 主子表循环块列数不统一 | 主表标题跨 A-G（7列），子表只用 B-F（5列）→ 预览时子表比主表窄，视觉不对齐 | 主表和子表必须使用**完全相同的列范围**（如都用 col0-col5）；主表标题 `merge:[0,5]`，子表表头和数据行也铺满同样的列范围 |
| 条形码/二维码 | 用 `displayConfig` + 单元格 `display/config` 实现；详见 `references/chart-components.md` §4-6 和 `references/report-design.md` §7 |
| `python -c` 跑到后台 | 命令自动进入 background，输出丢失，反复轮询浪费时间 | 永远 Write .py 文件后 `python /path/to/file.py` 执行，禁止 `python -c` |
| 预调外部 API 验证字段 | 网络请求慢或超时，白等 | 直接按用户提供的字段写脚本，不预调 API 验证 |
| Windows Python stdout GBK 编码 | `UnicodeEncodeError: 'gbk' codec` 导致脚本崩溃重试 | 每个脚本开头必须加：`import sys; sys.stdout.reconfigure(encoding='utf-8')` |
| 首次 save 后 sleep | `time.sleep()` 白白增加延迟 | 首次 `/save` 是同步请求，完成即可立即调 `save_db`，不需要任何 sleep |
| DB 凭证未知时猜测 | 连接失败→修改→重试，浪费多轮 | DB host/password 不确定时，写代码前先问用户，1 句话拿到信息比反复重试快得多 |
| DB 密码错误不立即问 | `Access denied` 后继续猜密码重试，耗费多轮 | 首次连接失败且密码来自记忆（可能过时），**立刻停下来问用户**，不要尝试其他密码 |
| 工具函数签名靠记忆 | `make_designer(name)` / `save_db(dbSource=...)` 等写错，运行才发现，多轮重试 | 写主脚本前先 `python -c "from jimureport_utils import X; help(X)"` 确认所有关键函数签名，不依赖文档示例或记忆 |
| graph.simple 误配 extData | 绑定数据集/设 apiStatus/设 dataId/设 dataId1 导致图表不渲染 | extData 只需 `{"chartId": layer_id, "chartType": "graph.simple"}`；节点+边全部内嵌 config 的 series[0].data/links；virtualCellRange 只放一行锚点；**不需要任何数据集** |
| Session base_url 缺 /jmreport | `session.request("/save",...)` 实际请求 `BASE_URL/save` 返回 404 | `Session` 初始化必须传含 `/jmreport` 的完整路径：`http://host:port/jmreport` |
| report_urls 参数顺序写反 | 预览链接指向错误 id | 正确签名：`report_urls(report_id, base_url)`，id 在前，base_url 在后 |
| 创建表达式报表前读多余文件 | 读 expressions.md + pitfalls.md + jimureport_utils.py = 多次 Read，超时 | 表达式报表：只需读 `references/expressions.md`（含全部函数）+ `references/pitfalls.md`，其余文件不用读 |
| 导入 `JimuSession` / `JimuReportSession` 等 | `ImportError: cannot import name 'JimuReportSession'`，整个脚本挂掉 | 唯一正确写法：`from jimureport_utils import Session, gen_id, gen_layer, make_styles, base_save, save_db, make_designer, chart_entry, virtual_row, print_summary, get_report, report_urls, parallel_save_dbs`；模块路径：`C:\Users\Administrator\.claude\skills\jimureport\scripts\jimureport_utils.py` |
| DBSUM/DBAVERAGE/DBMIN/DBMAX 不出数 | cell 里写了 `=DBSUM(ds.field)` 但预览结果为空，无报错 | `base_save` 必须同时传 `dbexps=["=DBSUM(ds.field)",...]`，引擎才会执行；修改已有报表时用 `dbexps=design.get("dbexps",[])` 透传，否则已有 DBSUM 也会失效 |
| 工具库模块名写错 | `from jimureport_session import JimuReportSession` 或 `from report_builder import ...` 均报 ModuleNotFoundError | 正确导入：`from jimureport_utils import Session, gen_id, gen_code, save_db, make_designer, base_save` |
| /save 新建报表 result.id 为 null | `resp["result"]["id"]` 返回 None，无法构造预览链接 | 新建时用 `gen_id()` 预生成 report_id，保存成功后直接用该 ID；`rid = resp["result"].get("id") or report_id` |
| 报表存在性验证走错接口 | `queryById`/`reportList`/`queryReportList` 均 404 或无权限 | 最简验证：`curl http://BASE/jmreport/index/{id}` 返回 HTML 即表示报表存在 |
| 循环块 db 别名与 dbCode 不一致 | 单元格绑定 `#{emp.field}` 但 dbCode 是 `emp_xxx`，预览数据全空 | `DB_ALIAS` 必须等于完整 dbCode；单元格 `#{alias.field}`、`loopBlockList.db`、`displayConfig` 的 text 三处保持一致 |
| API 分页数据集缺少分页参数 | 报表预览不分页或字段解析失败 | `api_url` 末尾带 `?pageSize='${pageSize}'&pageNo='${pageNo}'`（固定格式），`param_list` 加两条 `searchFlag=0` 的分页参数，**必须设默认值** `pageSize="20"`、`pageNo="1"`，留空不生效 |
| 表格 styles 未加边框 | 预览效果无边框，表格难以辨认 | 创建任何表格报表时，所有 style 对象**默认必须加边框**：`"border": {"bottom": ["thin","#BFBFBF"], "top": ["thin","#BFBFBF"], "left": ["thin","#BFBFBF"], "right": ["thin","#BFBFBF"]}`；标题行可用深色边框，数据行用灰色即可 |
| 多源报表误解为双独立表格或 loopBlock | 做成两个分开的表格/循环块，或用 loopBlockList 嵌套 → 主子字段无法同行显示 | 多源报表 = 同一数据行混合 `#{aa.*}`（主表）和 `#{bb.*}`（子表），引擎按子表记录数展开行，主表字段同行重复；**不需要 loopBlockList**；必须调 `/link/saveAndEdit` (linkType="4") 配置 mainField→subParam 关联 |
| save_db 省略 field_list | 调用报 TypeError（必填参数缺失） | `save_db` 第6个位置参数 `field_list` 为必填，不可省略；每个字段用 `{"fieldName":..,"fieldText":..,"widgetType":"String","isShow":"1","isQuery":"0"}` |
| 纵横组合动态列缺少二级子列表头 | 月份列下无"销售额/捐赠额"等标题，视觉混乱 | 需4行布局：标题行+双层表头行+数据行；row2 静态表头用 `merge:[1,0]` 纵跨2行，groupRight 用 `merge:[0,N-1]` 横跨N子列；row3 填静态子列名（在 groupRight 作用域内，引擎自动随月份重复）；row4 填 group+dynamic |
| 纵横组合 merges 只写标题不写静态表头跨行 | 静态表头（大区/省份）不合并，与子列行错位 | 必须同时写 `"B3:B4"` 等跨行合并 + `"D3:F3"` 等月份模板跨列合并，三处缺一不可 |
| groupRight 月份列头字母序错误 | "10月"排在"1月"前面（字母序："10月" < "1月"） | 月份字段用零填充：`CONCAT(LPAD(month_no,2,'0'),'月')` → "01月"~"12月"，字母序=时间序；不要用 `CONCAT(month_no,'月')` |
| `query_mysql` 执行 DML/DDL 数据不落库 | INSERT/DELETE/CREATE TABLE 看似成功但 COUNT 仍为 0 | `query_mysql` 内部无 `conn.commit()`，只适合 SELECT；**写数据必须直接用 pymysql**：`conn = pymysql.connect(...); cur.execute(...); conn.commit()` |
| MySQL 密码从 memory 或 get_ds_connection 猜测 | `Access denied` 后反复重试浪费多轮 | `get_ds_connection` 返回的密码可能加密；memory 记录的密码可能过时；**首次连接失败立刻停下来问用户**，不要尝试其他密码 |
| SQL 数据集 `field_list=[]` 传空 | 数据集保存成功但字段明细「暂无数据」，图表无法绑定字段 | 必须先调 `parse_sql(session, sql, db_source=ds_id)` 拿到字段列表再传给 `save_db`；不能传空数组 `[]` |
