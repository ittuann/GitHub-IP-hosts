"""Main script of the project.

This script is the main entry point for the project.
It fetches IP addresses for GitHub-related URLs using DNS-over-HTTPS APIs, processes the IP addresses,
and updates the README file with the latest IP addresses.

Functions:
    main():
        The main function that orchestrates the fetching, processing, and updating of IP addresses.

Note:
    File   : main.py
    Author : ittuann <ittuann@outlook.com> (https://github.com/ittuann)
    License: Apache-2.0 License.

Example:
    $ uv run python -m scripts.main --max_ips_per_url=3
"""

import argparse
import logging

from scripts.constants import DNS_API_CLOUDFLARE, DNS_API_GOOGLE, GITHUB_URLS, PROJECT_ROOT
from scripts.get_ip import get_all_ips
from scripts.process_ip import (
    format_host_strings,
    merge_deduplicate_ips,
    select_first_ip,
    select_limited_ips,
    sort_ips_by_latency,
)
from scripts.update_readme import get_hosts_head_str, update_readme


def main():
    """Main function of the script."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    parser = argparse.ArgumentParser(description="GitHub IP hosts")
    parser.add_argument("--max_ips_per_url", type=int, default=3, help="指定每个URL的最大IP地址数量")
    args = parser.parse_args()

    logging.info("通过 Cloudflare DNS-over-HTTPS 获取GitHub的IP地址")
    ips_cloudflare = get_all_ips(GITHUB_URLS, DNS_API_CLOUDFLARE)

    logging.info("通过 Google DNS-over-HTTPS 获取GitHub的IP地址")
    ips_google = get_all_ips(GITHUB_URLS, DNS_API_GOOGLE)

    logging.info("合并并去重两个 API 的 IP 地址")
    ips_merged = merge_deduplicate_ips(ips_cloudflare, ips_google)

    logging.info("按 TCP 443 连接耗时对每个 URL 的 IP 地址从快到慢排序")
    ips_res = sort_ips_by_latency(ips_merged)

    # 排序后每个 URL 的第一个 IP 即为最佳 IP
    ips_single = select_first_ip(ips_res)

    logging.info("格式化 hosts_single 字符串")
    host_single_strings = format_host_strings(ips_single)

    logging.info("写入 hosts_single 文件")
    with open(PROJECT_ROOT / "hosts_single", "w", encoding="utf-8") as file:
        file.write(get_hosts_head_str() + host_single_strings + "\n\n# GitHub IP hosts End\n")

    logging.info("限制每个 URL 的限定数量的 IP 地址")
    ips_res_limited = select_limited_ips(ips_res, args.max_ips_per_url)

    logging.info("格式化 host 字符串")
    host_strings = format_host_strings(ips_res_limited)

    logging.info("写入 hosts 文件")
    host_content = get_hosts_head_str() + host_strings + "\n\n# GitHub IP hosts End\n"
    with open(PROJECT_ROOT / "hosts", "w", encoding="utf-8") as file:
        file.write(host_content)

    print(host_content)

    logging.info("更新 README.md")
    update_readme("```\n" + host_content.strip() + "\n```")


if __name__ == "__main__":
    main()
