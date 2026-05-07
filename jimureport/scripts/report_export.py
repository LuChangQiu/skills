#!/usr/bin/env python3
"""
report_export.py — 积木报表导出/分享/导入 合并工具

用法：
  python report_export.py share --name 报表名 [--validity 1] [--lock 0]
  python report_export.py unshare --name 报表名 --share-id 分享记录ID
  python report_export.py export <report_id> [--format pdf] [--output ./out]
  python report_export.py import-excel <xlsx_path> [--name 报表名]
"""

import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))

import requests
from urllib.parse import quote
from jimureport_utils import Session, gen_code, make_designer, base_save

VALIDITY_MAP = {"永久": "1", "7天": "2", "1天": "3", "1": "1", "2": "2", "3": "3"}


# ── 分享 ─────────────────────────────────────────────────────────────

def share_report(base_url, token, name, validity="1", lock_status="0", lock_pwd="", verify="1", index=None):
    """根据名称查询报表并创建分享链接。"""
    session = Session(base_url, token)
    encoded = quote(name)
    resp = session.get(f"/query/report/folder?pageNo=1&pageSize=50&reportType=&name={encoded}&token={token}")
    records = resp.get("result", {}).get("records", [])
    if not records:
        print(f"未找到包含「{name}」的报表")
        return

    if len(records) == 1:
        target = records[0]
    elif index:
        target = records[index - 1]
    else:
        print(f"找到 {len(records)} 个报表，请用 --index N 指定：")
        for i, r in enumerate(records, 1):
            print(f"  [{i}] {r['name']}  (ID: {r['id']})")
        return

    result = session.request("/share/addAndEdit", {
        "id": "", "reportId": target["id"], "previewUrl": "", "previewLock": lock_pwd or ("1234" if lock_status == "1" else ""),
        "status": "0", "termOfValidity": validity, "previewLockStatus": lock_status, "verifyShareToken": verify,
    }).get("result", {})

    base_host = base_url.replace("/jmreport", "")
    share_url = f"{base_host}{result.get('previewUrl', '')}"
    print(f"分享成功: {target['name']}")
    print(f"  链接: {share_url}")
    if lock_status == "1":
        print(f"  密码: {result.get('previewLock', lock_pwd)}")


def query_share(session, report_id):
    """查询报表的当前分享记录，返回 result dict 或 None。"""
    resp = session.get(f"/share/queryJurisdiction?reportId={report_id}")
    return resp.get("result")


def unshare_report(base_url, token, report_id=None, share_id=None, name=None):
    """取消报表分享（status=1 禁用）。支持按名称自动查 share_id。"""
    session = Session(base_url, token)

    if name and not report_id:
        encoded = quote(name)
        resp = session.get(f"/query/report/folder?pageNo=1&pageSize=50&reportType=&name={encoded}&token={token}")
        records = resp.get("result", {}).get("records", [])
        if not records:
            print(f"未找到包含「{name}」的报表")
            return
        if len(records) > 1:
            print(f"找到 {len(records)} 个报表，请用 --report-id 指定：")
            for r in records:
                print(f"  {r['name']}  (ID: {r['id']})")
            return
        report_id = records[0]["id"]

    if not share_id:
        share = query_share(session, report_id)
        if not share:
            print(f"该报表暂无分享记录: reportId={report_id}")
            return
        share_id = share["id"]

    result = session.request("/share/addAndEdit", {
        "id": share_id, "reportId": report_id, "status": "1",
    })
    if result.get("success"):
        print(f"取消分享成功: reportId={report_id}, shareId={share_id}")
    else:
        print(f"取消失败: {result.get('message')}")


# ── 导出 ─────────────────────────────────────────────────────────────

def export_report(base_url, token, report_id, fmt="pdf", output_dir=".",
                  tenant_id="1000", sheet_id="default"):
    """
    导出报表为 PDF/Excel/Word。

    实测接口（POST + 签名）：
      pdf   → /exportPdfStream
      excel → /exportAllExcelStream
      word  → /export/word
    旧版常见的 /exportPdf、/exportXls、/exportWord (GET) 已不存在，会返回
    `No static resource jmreport/exportXls.` 类错误。
    """
    import time
    from jimureport_core import _compute_sign

    path_map = {
        "pdf":   "/exportPdfStream",
        "excel": "/exportAllExcelStream",
        "word":  "/export/word",
    }
    ext_map = {"pdf": ".pdf", "excel": ".xlsx", "word": ".docx"}
    if fmt not in path_map:
        print(f"不支持的格式: {fmt}，可选: pdf/excel/word")
        return

    payload = {
        "excelConfigId": report_id,
        "sheetId": sheet_id,
        "queryParam": {
            "token": token, "tenantId": tenant_id,
            "pageNo": "1", "pageSize": 10,
            "customTableTitleSorts": [],
            "currentPageNo": "1", "currentPageSize": 10,
        },
    }
    headers = {
        "X-Access-Token":     token,
        "token":              token,
        "tenantid":           tenant_id,
        "jmreport-tenant-id": tenant_id,
        "X-TIMESTAMP":        str(int(time.time() * 1000)),
        "X-Sign":             _compute_sign(payload),
        "Content-Type":       "application/json;charset=UTF-8",
    }
    sess = requests.Session()
    sess.trust_env = False
    resp = sess.post(base_url + path_map[fmt], json=payload, headers=headers,
                     stream=True, proxies={})
    resp.raise_for_status()

    ct = resp.headers.get("Content-Type", "")
    if "application/json" in ct.lower():
        print(f"导出失败: {resp.text[:300]}")
        return

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{report_id}{ext_map[fmt]}")
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)
    print(f"导出成功: {out_path}")


# ── 导出报表配置（跨环境迁移包，对应 UI「导出报表配置」按钮）──────────

def export_report_config(base_url, token, report_id, output_dir=".",
                         tenant_id="1000", as_readable=False):
    """
    导出报表配置 JSON（用于跨环境迁移 / import 还原）。

    实测接口：GET /jmreport/exportReportConfig?id={id}&token={token}
    需签名（X-Sign + X-TIMESTAMP，已加入 SIGNED_PATHS）。

    响应：{success, code, result: {file: <base64>}}
      - file 字段是 base64 编码的迁移包字符串
      - base64 解码后是 URL-encoded 的 JSON：{"jimu_report_db_list": "...", "jimu_report": "..."}
      - 这就是 jmreport 的 import 接口可识别的格式

    生成 2 份文件：
      - <id>_config.json          标准迁移包（可直接 import 还原）
      - <id>_config.readable.json （可选）展开 URL 编码的可读版本
    """
    import time, base64, urllib.parse
    from jimureport_core import _compute_sign

    params = {"id": report_id, "token": token}
    headers = {
        "X-Access-Token":     token,
        "token":              token,
        "tenantid":           tenant_id,
        "jmreport-tenant-id": tenant_id,
        "X-TIMESTAMP":        str(int(time.time() * 1000)),
        "X-Sign":             _compute_sign(params),
        "Accept":             "application/json",
    }
    sess = requests.Session(); sess.trust_env = False
    r = sess.get(base_url + "/exportReportConfig", params=params,
                 headers=headers, proxies={})
    r.raise_for_status()
    body = r.json()
    if not body.get("success"):
        print(f"导出失败: {body.get('message')}")
        return

    file_b64 = body["result"]["file"]
    decoded = base64.b64decode(file_b64).decode("utf-8")

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{report_id}_config.json")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(decoded)
    print(f"导出成功（迁移包）: {out_path}")

    if as_readable:
        parsed = json.loads(decoded)
        readable = {k: json.loads(urllib.parse.unquote(v)) for k, v in parsed.items()}
        readable_path = os.path.join(output_dir, f"{report_id}_config.readable.json")
        with open(readable_path, "w", encoding="utf-8") as f:
            json.dump(readable, f, ensure_ascii=False, indent=2)
        print(f"可读版本: {readable_path}")


def import_report_config(base_url, token, file_path):
    """
    导入报表配置（迁移包，对应 UI「导入报表配置」按钮）。

    实测接口：POST /jmreport/importReportConfig (multipart)
    上传文件内容 = export_report_config 落盘的解码后 url-encoded JSON 字符串
    （**不是** base64 原文 —— 平台前端 download 行为是先解码再保存）。
    """
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return
    session = Session(base_url, token)
    with open(file_path, "rb") as f:
        r = session.upload("/importReportConfig",
                           files={"file": (os.path.basename(file_path), f, "application/json")})
    if r.get("success"):
        print(f"导入成功: {r.get('result') or r.get('message')}")
    else:
        print(f"导入失败: {r.get('message')} | code={r.get('code')}")


# ── 导入 Excel ──────────────────────────────────────────────────────

def import_excel(base_url, token, xlsx_path, name=None):
    """上传 Excel 文件导入为积木报表。"""
    session = Session(base_url, token)
    if not name:
        name = os.path.splitext(os.path.basename(xlsx_path))[0]

    with open(xlsx_path, "rb") as f:
        result = session.upload("/importExcel", files={"file": (os.path.basename(xlsx_path), f)})
    if not result.get("success"):
        print(f"导入失败: {result.get('message')}")
        return

    parsed = result["result"]
    save_resp = session.request("/save", base_save("", make_designer("", name)))
    report_id = save_resp["result"]["id"]

    overrides = {}
    for k in ["rows", "cols", "styles", "merges"]:
        if k in parsed:
            overrides[k] = parsed[k]
    session.request("/save", base_save(report_id, make_designer(report_id, name), **overrides))
    print(f"导入成功: {name} (ID: {report_id})")
    print(f"  设计器: {base_url}/index/{report_id}")


# ── CLI ──────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="积木报表导出/分享/导入工具")
    p.add_argument("--base-url", default=os.environ.get("JMREPORT_URL", "<api_base>"))
    p.add_argument("--token", default=os.environ.get("JMREPORT_TOKEN", ""))
    sub = p.add_subparsers(dest="cmd")

    sh = sub.add_parser("share", help="创建分享链接")
    sh.add_argument("--name", required=True)
    sh.add_argument("--validity", default="1")
    sh.add_argument("--lock", default="0")
    sh.add_argument("--password", default="")
    sh.add_argument("--index", type=int, default=None)

    us = sub.add_parser("unshare", help="取消分享链接")
    us.add_argument("--name", default=None, help="报表名称（自动查 report_id 和 share_id）")
    us.add_argument("--report-id", default=None)
    us.add_argument("--share-id", default=None)

    ex = sub.add_parser("export", help="导出 PDF/Excel/Word")
    ex.add_argument("report_id")
    ex.add_argument("--format", default="pdf", choices=["pdf", "excel", "word"])
    ex.add_argument("--output", default=".")

    ec = sub.add_parser("export-config", help="导出报表配置 JSON（迁移包，可 import 还原）")
    ec.add_argument("report_id")
    ec.add_argument("--output", default=".")
    ec.add_argument("--readable", action="store_true", help="同时生成展开 URL 编码的可读版本")
    ec.add_argument("--tenant", default="1000")

    im = sub.add_parser("import-excel", help="导入 Excel 模板")
    im.add_argument("xlsx_path")
    im.add_argument("--name", default=None)

    ic = sub.add_parser("import-config", help="导入报表配置（迁移包 .json）")
    ic.add_argument("file_path")

    args = p.parse_args()
    if args.cmd == "share":
        share_report(args.base_url, args.token, args.name, args.validity, args.lock, args.password, index=args.index)
    elif args.cmd == "unshare":
        unshare_report(args.base_url, args.token, report_id=args.report_id, share_id=args.share_id, name=args.name)
    elif args.cmd == "export":
        export_report(args.base_url, args.token, args.report_id, args.format, args.output)
    elif args.cmd == "export-config":
        export_report_config(args.base_url, args.token, args.report_id,
                             args.output, tenant_id=args.tenant, as_readable=args.readable)
    elif args.cmd == "import-excel":
        import_excel(args.base_url, args.token, args.xlsx_path, args.name)
    elif args.cmd == "import-config":
        import_report_config(args.base_url, args.token, args.file_path)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
