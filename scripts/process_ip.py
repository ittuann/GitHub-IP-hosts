"""Process IP addresses.

This module contains functions for processing IP addresses.

Note:
    File   : process_ip.py
    Author : ittuann <ittuann@outlook.com> (https://github.com/ittuann)
    License: Apache-2.0 License.
"""

import logging
import socket
import time

from scripts.get_ip import URLIPMapping

TCP_PORT = 443
TCP_TIMEOUT = 2.0
TCP_ATTEMPTS = 3


def tcp_latency(
    ip: str, port: int = TCP_PORT, timeout: float = TCP_TIMEOUT, attempts: int = TCP_ATTEMPTS
) -> float | None:
    """测量到指定IP的TCP连接耗时 (秒)。

    Parameters:
        ip (str): 目标IP地址。
        port (int): 目标端口 默认为443。
        timeout (float): 单次连接超时时间 (秒)。
        attempts (int): 尝试次数 取成功连接中的最小耗时。

    Returns:
        float | None: 最小连接耗时 全部失败时返回None。
    """
    best: float | None = None
    for _ in range(attempts):
        start = time.perf_counter()
        try:
            with socket.create_connection((ip, port), timeout=timeout):
                elapsed = time.perf_counter() - start
        except OSError:
            continue
        if best is None or elapsed < best:
            best = elapsed
    return best


def sort_ips_by_latency(ip_list: list[URLIPMapping]) -> list[URLIPMapping]:
    """按TCP连接耗时对每个URL的所有IP地址从快到慢排序 不丢弃任何IP。

    无法连接的IP (以及DNS解析失败的占位项) 排在该URL的最后 并保持原有相对顺序。
    结果按URL排序 同一URL内按耗时升序。URL下只有一个IP时原样保留。

    Parameters:
        ip_list (List[URLIPMapping]): 包含URL和IP地址的列表。

    Returns:
        List[URLIPMapping]: 排序后的列表 包含输入中的所有记录。
    """
    ips_per_url: dict[str, list[str]] = {}
    for record in ip_list:
        ips = ips_per_url.setdefault(record.url, [])
        if record.ip not in ips:
            ips.append(record.ip)

    result: list[URLIPMapping] = []
    for url in sorted(ips_per_url):
        ips = ips_per_url[url]
        latencies: dict[str, float] = {}
        for ip in ips:
            # DNS解析失败时的占位项 (如 "# ") 不是真实IP 无需测速
            if ip.strip().startswith("#"):
                continue
            latency = tcp_latency(ip)
            logging.info(f"{url} - {ip}: TCP {TCP_PORT} 连接耗时: {latency}")
            if latency is not None:
                latencies[ip] = latency

        # sorted 是稳定排序 不可达的IP保持原顺序排在最后
        ordered = sorted(ips, key=lambda ip: latencies.get(ip, float("inf")))
        if latencies:
            best = ordered[0]
            logging.info(f"{url} 最佳IP地址: {best}, 延迟: {latencies[best]}")
        else:
            logging.warning(f"{url} 无法找到可连接的IP地址")
        result.extend(URLIPMapping(url, ip) for ip in ordered)

    return result


def select_first_ip(ip_list: list[URLIPMapping]) -> list[URLIPMapping]:
    """选择每个URL的第一个IP地址。

    GitHub runners are placed in Azure. Ping doesn't work in azure by design.
    https://github.com/actions/runner-images/issues/1519#issuecomment-752644218

    Parameters:
        ip_list (List[Dict[str, str]]): 包含URL和IP地址的字典列表。

    Returns:
        List[Dict[str, str]]: 包含URL和第一个IP地址的字典列表。
    """
    first_ips: dict[str, str] = {}
    for record in ip_list:
        if record.url not in first_ips:
            first_ips[record.url] = record.ip
            logging.info(f"{record.url} 第一个IP地址: {record.ip}")

    return [URLIPMapping(url, ip) for url, ip in first_ips.items()]


def select_limited_ips(ip_list: list[URLIPMapping], max_ips_per_url: int = 3) -> list[URLIPMapping]:
    """选择每个URL的限定数量的IP地址

    Parameters:
        ip_list (List[Dict[str, str]]): 包含URL和IP地址的字典列表。
        max_ips_per_url (int): 每个URL允许的最大IP地址数量 默认为4。

    Returns:
        List[Dict[str, str]]: 根据限定数量选择的URL和IP地址的字典列表。
    """
    ips_per_url: dict[str, list[str]] = {}
    for record in ip_list:
        if record.url not in ips_per_url:
            ips_per_url[record.url] = [record.ip]
        elif len(ips_per_url[record.url]) < max_ips_per_url:
            ips_per_url[record.url].append(record.ip)

    result: list[URLIPMapping] = []
    for url, ips in ips_per_url.items():
        for ip in ips:
            result.append(URLIPMapping(url, ip))

    return result


def merge_deduplicate_ips(ips1: list[URLIPMapping], ips2: list[URLIPMapping]) -> list[URLIPMapping]:
    """合并并去重从两个API得到的IP地址。

    Parameters:
        ips1 (List[Dict[str, str]]): 从第一个API得到的IP地址列表。
        ips2 (List[Dict[str, str]]): 从第二个API得到的IP地址列表。

    Returns:
        List[Dict[str, str]]: 合并并去重后按URL排序的IP地址列表。
    """
    combined_ips: set[tuple[str, str]] = {(record.url, record.ip) for record in ips1}
    combined_ips.update({(record.url, record.ip) for record in ips2})

    sorted_ips: list[tuple[str, str]] = sorted(combined_ips, key=lambda x: (x[0], x[1]))
    return [URLIPMapping(url, ip) for url, ip in sorted_ips]


def format_host_strings(ip_list: list[URLIPMapping]) -> str:
    """将列表中的字典中的IP地址和URL转换为host格式的字符串 并确保每个URL的开头对齐。

    Parameters:
        ip_list (List[Dict[str, str]]): 包含URL和IP地址的字典列表。

    Returns:
        str: 包含host格式的字符串。
    """
    host_strings: list[str] = []
    max_ip_length = max((len(record.ip) for record in ip_list), default=0)
    for record in ip_list:
        host_format = f"{record.ip.ljust(max_ip_length)} {record.url}"
        host_strings.append(host_format)

    return "\n".join(host_strings)
