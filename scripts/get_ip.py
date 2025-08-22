"""Records the IP addresses.

This script fetches and records the IP addresses of various GitHub-related URLs using DNS-over-HTTPS APIs.

Note:
    File   : get_ip.py
    Author : ittuann <ittuann@outlook.com> (https://github.com/ittuann)
    License: Apache-2.0 License.
"""

import logging
import time
from dataclasses import dataclass

import requests  # type: ignore
from pydantic import BaseModel, Field, HttpUrl, ValidationError


class DNSRecord(BaseModel):
    """A dictionary type for storing DNS record information."""

    name: str
    type: int
    ttl: int = Field(alias="TTL")
    data: str


@dataclass
class URLIPMapping:
    """Class for storing URL and IP address mappings."""

    def __init__(self, url: str, ip: str):
        """Initialize the URL and IP address mapping."""
        if not isinstance(url, str) or not isinstance(ip, str):
            raise TypeError("url and ip must be of type str")
        self.url = url
        self.ip = ip

    def to_dict(self) -> dict[str, str]:
        """Convert the URLIPMapping object to a dictionary."""
        return {self.url: self.ip}

    def __repr__(self):
        """Return a string representation of the URLIPMapping object. __str__ is also set to this method."""
        return f"URLIPMapping(url='{self.url}', ip='{self.ip}')"


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


def validate_ip(ip: str):
    """简易验证给定的字符串是否是一个有效的 IP 地址。

    Raises:
        ValueError: IP地址无效
    """
    parts = ip.split(".")
    if len(parts) != 4:
        raise ValueError(f"无效的 IP 地址: {ip}")
    for part in parts:
        if not part.isdigit() or not (0 <= int(part) <= 255):
            raise ValueError(f"无效的 IP 地址: {ip}")


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

            # 验证得到的每个IP地址
            for record in records:
                try:
                    validate_ip(record.data)
                except ValueError as e:
                    logging.warning(f"无效的 IP 地址: {record.data} - {e}")
                    records.remove(record)

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


def get_all_ips(urls: list[str], dns_api: str, retries_num: int = 3) -> list[URLIPMapping]:
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
    results: list[URLIPMapping] = []

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

            results.extend(URLIPMapping(url, record.data) for record in records)

        except RuntimeError as e:
            logging.error(f"{url} 无法解析IP地址: {e}")
            results.append(URLIPMapping(url, "# "))

    return results
