"""Records the IP addresses."""

import logging
import time
from typing import Dict, List, TypedDict

import requests  # type: ignore


class DNSRecord(TypedDict):
    """DNS record dictionary."""

    name: str
    type: int
    TTL: int
    data: str


def fetch_dns_records(dns_api: str, url: str, retries_num: int = 3) -> List[DNSRecord]:
    """使用Cloudflare的DNS-over-HTTPS API获取指定URL的A记录。

    Parameters:
        dns_api (str): DNS-over-HTTPS API的URL。
        url (str): 要解析的URL。
        retries_num (int): 最大重试次数。

    Raises:
        RuntimeError: 无法完成GET请求。

    Returns:
        List[DNSRecord]: 包含A记录的字典列表。
    """
    for attempt_num in range(1, retries_num + 1):
        try:
            response = requests.get(
                dns_api,
                headers={"accept": "application/dns-json"},
                params={"name": url, "type": "A"},
            )
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()
            return [answer for answer in data.get("Answer", []) if answer["type"] == 1]

        except requests.Timeout as e:
            logging.warning(f"请求超时 ({attempt_num}/{retries_num}): {e}")
            if attempt_num < retries_num:
                logging.warning("等待 1 秒后重试...")
                time.sleep(1)
        except requests.RequestException as e:
            logging.warning(f"{url} 请求失败 ({attempt_num}/{retries_num}): {type(e).__name__} - {e}")

        if attempt_num >= retries_num:
            logging.error(f"{url}: 在 {retries_num} 次尝试后无法完成请求")
            raise RuntimeError(f"{url}: 在 {retries_num} 次尝试后无法完成请求")
    # 如果所有尝试都失败则返回一个空列表
    return []


def get_all_ips(urls: List[str], dns_api: str, retries_num: int = 3) -> List[Dict[str, str]]:
    """获取每个URL的最佳IP地址。

    Parameters:
        urls (List[str]): 要解析的URL列表。
        dns_api (str): DNS-over-HTTPS API的URL。
        retries_num (int): 最大重试次数。

    Raises:
        RuntimeError: 无法获取记录。

    Returns:
        List[Dict[str, str]]: 包含URL和最佳IP地址的字典列表。
    """
    results = []

    # 解析每个URL的IP地址
    for url in urls:
        try:
            answers = fetch_dns_records(dns_api, url, retries_num)

            # 打印得到的A记录数量
            logging.info(f"{url} 得到 {len(answers)} 个A记录")
            for idx, answer in enumerate(answers, start=1):
                logging.info(f"{url} - {idx}: {answer['data']}, TTL: {answer['TTL']}")

            for answer in answers:
                results.append({"url": url, "ip": answer["data"]})

        except RuntimeError as e:
            logging.error(f"{url} 无法获取记录：{e}")
            results.append({"url": url, "ip": "# "})

    return results
