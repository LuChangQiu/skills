"""
jimureport_link.py — 钻取/联动配置
"""
import json
from concurrent.futures import ThreadPoolExecutor

from jimureport_core import Session


def create_link(
    session: Session,
    report_id: str,
    link_name: str,
    link_type: str,
    parameter_list: list[dict],
    *,
    target_report_id: str = "",
    link_chart_id: str = "",
    api_url: str = "",
    eject_type: str = "0",
) -> str:
    """
    创建钻取/联动配置，返回 linkId。
    link_type: "0"=报表钻取 / "1"=网络链接 / "2"=图表联动
    """
    payload = {
        "linkName":    link_name,
        "linkType":    link_type,
        "reportId":    target_report_id if link_type == "0" else report_id,
        "ejectType":   eject_type,
        "apiUrl":      api_url,
        "apiMethod":   "",
        "requirement": "",
        "linkChartId": link_chart_id,
        "parameter":   json.dumps(parameter_list, ensure_ascii=False),
    }
    r = session.request("/link/saveAndEdit", payload)
    return r["result"]


def parallel_create_links(session: Session, link_configs: list[dict]) -> list[str]:
    with ThreadPoolExecutor(max_workers=len(link_configs)) as ex:
        futures = [ex.submit(create_link, session, **cfg) for cfg in link_configs]
        return [f.result() for f in futures]
