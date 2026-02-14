"""Process IP addresses.

This module contains functions for processing IP addresses.

Note:
    File   : process_ip.py
    Author : ittuann <ittuann@outlook.com> (https://github.com/ittuann)
    License: Apache-2.0 License.
"""

import logging

from ping3 import ping  # type: ignore

from scripts.get_ip import URLIPMapping


def select_best_ip(ip_list: list[URLIPMapping]) -> list[URLIPMapping]:
    """选择每个URL的最佳IP地址。

    Parameters:
        ip_list (List[Dict[str, str]]): 包含URL和IP地址的字典列表。

    Returns:
        List[Dict[str, str]]: 包含URL和最佳IP地址的字典列表。
    """
    best_ips: list[URLIPMapping] = []
    url_respond_ips: dict[str, list[str]] = {}

    # 存储每个URL对应的所有IP地址
    for record in ip_list:
        if record.url not in url_respond_ips:
            url_respond_ips[record.url] = []
        url_respond_ips[record.url].append(record.ip)

    # 为每个URL选择最佳IP地址
    for url, ips in url_respond_ips.items():
        best_ip: str | None = None
        lowest_latency: float = float("inf")
        for ip in ips:
            latency = ping(ip, timeout=1)
            logging.info(f"{url} - {ip}: 延迟: {latency}")
            if latency is not None and latency < lowest_latency:
                lowest_latency = latency
                best_ip = ip

        if best_ip is not None:
            best_ips.append(URLIPMapping(url, best_ip))
            logging.info(f"{url} 最佳IP地址: {best_ip}, 延迟: {lowest_latency}")
        else:
            logging.warning(f"{url} 无法找到最佳IP地址")

    return best_ips


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


def reorder_ips_with_best_first(ips_merged: list[URLIPMapping], ips_best: list[URLIPMapping]) -> list[URLIPMapping]:
    """重新排序IP地址列表 将每个URL的最佳IP地址放置在前面。

    Parameters:
        ips_merged (List[Dict[str, str]]): 合并并去重后的IP地址列表 按URL和IP字典序排序。
        ips_best (List[Dict[str, str]]): 每个URL的最佳IP地址列表。

    Returns:
        List[Dict[str, str]]: 重新排序后的IP地址列表 每个URL的最佳IP地址位于前面。
    """
    url_to_best_ip: dict[str, str] = {}
    for record in ips_best:
        url_to_best_ip.update(record.to_dict())
    ips_res: list[URLIPMapping] = []

    # 先添加最佳IP
    for record in ips_merged:
        if record.url in url_to_best_ip:
            ips_res.append(URLIPMapping(record.url, url_to_best_ip[record.url]))
            del url_to_best_ip[record.url]
    # 再添加其他IP
    for record in ips_merged:
        if record not in ips_res:
            ips_res.append(record)
    ips_res = sorted(ips_res, key=lambda x: x.url)
    return ips_res


def format_host_strings(ip_list: list[URLIPMapping]) -> str:
    """将列表中的字典中的IP地址和URL转换为host格式的字符串 并确保每个URL的开头对齐。

    Parameters:
        ip_list (List[Dict[str, str]]): 包含URL和IP地址的字典列表。

    Returns:
        str: 包含host格式的字符串。
    """
    host_strings: list[str] = []
    max_ip_length = max(len(record.ip) for record in ip_list)
    for record in ip_list:
        host_format = f"{record.ip.ljust(max_ip_length)} {record.url}"
        host_strings.append(host_format)

    return "\n".join(host_strings)
