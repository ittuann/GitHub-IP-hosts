"""Process IP addresses.

This module contains functions for processing IP addresses.

Note:
    File   : process_ip.py
    Author : ittuann <ittuann@outlook.com>
    License: MIT License.
"""

import logging

from ping3 import ping  # type: ignore


def select_best_ip(ip_list: list[dict[str, str]]) -> list[dict[str, str]]:
    """选择每个URL的最佳IP地址。

    Parameters:
        ip_list (List[Dict[str, str]]): 包含URL和IP地址的字典列表。

    Returns:
        List[Dict[str, str]]: 包含URL和最佳IP地址的字典列表。
    """
    best_ips = []
    url_to_ips: dict[str, list[str]] = {}

    for record in ip_list:
        url = record["url"]
        ip = record["ip"]
        if url not in url_to_ips:
            url_to_ips[url] = []
        url_to_ips[url].append(ip)

    for url, ips in url_to_ips.items():
        best_ip = None
        lowest_latency = float("inf")
        for ip in ips:
            latency = ping(ip, timeout=1)
            logging.info(f"{url} - {ip}: 延迟: {latency}")
            if latency is not None and latency < lowest_latency:
                lowest_latency = latency
                best_ip = ip

        if best_ip is not None:
            best_ips.append({"url": url, "ip": best_ip})
            logging.info(f"{url} 最佳IP地址: {best_ip}, 延迟: {lowest_latency}")
        else:
            logging.warning(f"{url} 无法找到最佳IP地址")

    return best_ips


def select_first_ip(ip_list: list[dict[str, str]]) -> list[dict[str, str]]:
    """选择每个URL的第一个IP地址。

    GitHub runners are placed in Azure. Ping doesn't work in azure by design.
    https://github.com/actions/runner-images/issues/1519#issuecomment-752644218

    Parameters:
        ip_list (List[Dict[str, str]]): 包含URL和IP地址的字典列表。

    Returns:
        List[Dict[str, str]]: 包含URL和第一个IP地址的字典列表。
    """
    first_ips = {}
    for record in ip_list:
        url, ip = record["url"], record["ip"]
        if url not in first_ips:
            first_ips[url] = ip
            logging.info(f"{url} 第一个IP地址: {ip}")

    return [{"url": url, "ip": ip} for url, ip in first_ips.items()]


def select_limited_ips(ip_list: list[dict[str, str]], max_ips_per_url: int = 4) -> list[dict[str, str]]:
    """选择每个URL的限定数量的IP地址

    Parameters:
        ip_list (List[Dict[str, str]]): 包含URL和IP地址的字典列表。
        max_ips_per_url (int): 每个URL允许的最大IP地址数量 默认为4。

    Returns:
        List[Dict[str, str]]: 根据限定数量选择的URL和IP地址的字典列表。
    """
    ips_per_url = {}
    for record in ip_list:
        url, ip = record["url"], record["ip"]
        if url not in ips_per_url:
            ips_per_url[url] = [ip]
        elif len(ips_per_url[url]) < max_ips_per_url:
            ips_per_url[url].append(ip)

    result = []
    for url, ips in ips_per_url.items():
        for ip in ips:
            result.append({"url": url, "ip": ip})

    return result


def merge_deduplicate_ips(ips1: list[dict[str, str]], ips2: list[dict[str, str]]) -> list[dict[str, str]]:
    """合并并去重从两个API得到的IP地址。

    Parameters:
        ips1 (List[Dict[str, str]]): 从第一个API得到的IP地址列表。
        ips2 (List[Dict[str, str]]): 从第二个API得到的IP地址列表。

    Returns:
        List[Dict[str, str]]: 合并并去重后按URL排序的IP地址列表。
    """
    combined_ips = {(record["url"], record["ip"]) for record in ips1}
    combined_ips.update({(record["url"], record["ip"]) for record in ips2})
    sorted_ips = sorted(combined_ips, key=lambda x: (x[0], x[1]))
    return [{"url": url, "ip": ip} for url, ip in sorted_ips]


def reorder_ips_with_best_first(
    ips_merged: list[dict[str, str]], ips_best: list[dict[str, str]]
) -> list[dict[str, str]]:
    """重新排序IP地址列表 将每个URL的最佳IP地址放置在前面。

    Parameters:
        ips_merged (List[Dict[str, str]]): 合并并去重后的IP地址列表 按URL和IP字典序排序。
        ips_best (List[Dict[str, str]]): 每个URL的最佳IP地址列表。

    Returns:
        List[Dict[str, str]]: 重新排序后的IP地址列表 每个URL的最佳IP地址位于前面。
    """
    url_to_best_ip = {record["url"]: record["ip"] for record in ips_best}
    ips_res = []
    for record in ips_merged:
        url = record["url"]
        if url in url_to_best_ip:
            ips_res.append({"url": url, "ip": url_to_best_ip[url]})
            del url_to_best_ip[url]
    for record in ips_merged:
        if record not in ips_res:
            ips_res.append(record)
    ips_res = sorted(ips_res, key=lambda x: x["url"])
    return ips_res


def format_host_strings(ip_list: list[dict[str, str]]) -> str:
    """将列表中的字典中的IP地址和URL转换为host格式的字符串 并确保每个URL的开头对齐。

    Parameters:
        ip_list (List[Dict[str, str]]): 包含URL和IP地址的字典列表。

    Returns:
        str: 包含host格式的字符串。
    """
    host_strings = []
    max_ip_length = max(len(record["ip"]) for record in ip_list)
    for record in ip_list:
        host_format = f"{record['ip'].ljust(max_ip_length)} {record['url']}"
        host_strings.append(host_format)

    return "\n".join(host_strings)
