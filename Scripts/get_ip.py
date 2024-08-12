"""Records the IP addresses.

This script fetches and records the IP addresses of various GitHub-related URLs using DNS-over-HTTPS APIs.

Note:
    File   : get_ip.py
    Author : ittuann <ittuann@outlook.com>
    License: MIT License.
"""

import logging
import time

import requests  # type: ignore
from pydantic import BaseModel, Field, HttpUrl, ValidationError


class DNSRecord(BaseModel):
    """A dictionary type for storing DNS record information."""

    name: str
    type: int
    ttl: int = Field(alias="TTL")
    data: str


def validate_str_url(url: str):
    """验证给定的字符串是否是一个有效的 URL。

    Raises:
        ValueError: URL无效
    """
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"  # 补充添加https协议头验证
    try:
        # 只尝试创建 HttpUrl 以验证
        # 不会返回 HttpUrl 对象
        _ = HttpUrl(url=url)
    except ValidationError as e:
        logging.error(f"无效的 URL: {url}, 错误信息: {str(e)}")
        raise ValueError(f"无效的 URL: {url}") from e


def fetch_dns_records(dns_api: str, url: str, retries_num: int = 3) -> list[DNSRecord]:
    """使用DNS-over-HTTPS API获取指定URL的A记录。

    Parameters:
        dns_api (str): DNS-over-HTTPS API的URL。
        url (str): 要解析的URL。
        retries_num (int): 最大重试次数。

    Raises:
        ValueError: API或URL无效。
        RuntimeError: 无法完成GET请求。

    Returns:
        List[DNSRecord]: 包含A记录的字典列表。
    """
    try:
        validate_str_url(dns_api)
        validate_str_url(url)
    except ValueError as e:
        logging.error(f"URL 验证无效: {e}")
        raise ValueError(f"无效的 URL: {e}") from e

    for attempt_num in range(1, retries_num + 1):
        try:
            response = requests.get(
                dns_api,
                headers={"accept": "application/dns-json"},
                params={"name": url, "type": "A"},
            )
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()
            records = [DNSRecord(**answer) for answer in data.get("Answer", []) if answer["type"] == 1]
            return records

        except requests.Timeout as e:
            logging.warning(f"请求超时 ({attempt_num}/{retries_num}): {e}")
            time.sleep(1)
        except requests.RequestException as e:
            logging.warning(f"{url} 请求失败 ({attempt_num}/{retries_num}): {type(e).__name__} - {e}")
            time.sleep(1)
        except ValidationError as e:
            logging.error(f"Pydantic 数据验证失败: {e}")
            return []

        if attempt_num >= retries_num:
            logging.error(f"{url}: 在 {retries_num} 次尝试后无法完成请求")
            raise RuntimeError(f"{url}: 在 {retries_num} 次尝试后无法完成请求")
    # 如果所有尝试都失败则返回一个空列表
    return []


def get_all_ips(urls: list[str], dns_api: str, retries_num: int = 3) -> list[dict[str, str]]:
    """获取指定URL列表的IP地址

    Parameters:
        urls (List[str]): 要解析的URL列表。
        dns_api (str): DNS-over-HTTPS API的URL。
        retries_num (int): 最大重试次数。

    Raises:
        RuntimeError: 无法获取记录。

    Returns:
        List[Dict[str, str]]: 包含URL和IP地址的字典列表。
    """
    results: list[dict[str, str]] = []

    # 解析每个URL的IP地址
    for url in urls:
        try:
            records = fetch_dns_records(dns_api, url, retries_num)

            # 检查records是否为空
            if not records:
                raise RuntimeError(f"没有得到 {url} 的任何A记录")

            # 打印得到的A记录数量
            logging.info(f"{url} 得到 {len(records)} 个A记录")
            for idx, record in enumerate(records, start=1):
                logging.info(f"{url} - {idx}: {record.data}, TTL: {record.ttl}")

            results.extend({"url": url, "ip": record.data} for record in records)

        except RuntimeError as e:
            logging.error(f"{url} 无法解析IP地址: {e}")
            results.append({"url": url, "ip": "# "})

    return results
