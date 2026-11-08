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
    $ uv run python -m scripts.main --max_ips_per_url=3 --is_in_gha=False
"""

import argparse
import logging

from scripts.constants import DNS_API_CLOUDFLARE, DNS_API_GOOGLE, GITHUB_URLS, PROJECT_ROOT
from scripts.get_ip import get_all_ips
from scripts.process_ip import (
    format_host_strings,
    merge_deduplicate_ips,
    reorder_ips_with_best_first,
    select_best_ip,
    select_first_ip,
    select_limited_ips,
)
from scripts.update_readme import get_hosts_head_str, update_readme


def main():
    """Main function of the script."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    parser = argparse.ArgumentParser(description="GitHub IP hosts")
    parser.add_argument("--is_in_gha", type=bool, default=False, help="指定是否在GitHub Actions环境中运行")
    parser.add_argument("--max_ips_per_url", type=int, default=3, help="指定每个URL的最大IP地址数量")
    args = parser.parse_args()

    logging.info("通过 Cloudflare DNS-over-HTTPS 获取GitHub的IP地址")
    ips_cloudflare = get_all_ips(GITHUB_URLS, DNS_API_CLOUDFLARE)

    logging.info("通过 Google DNS-over-HTTPS 获取GitHub的IP地址")
    ips_google = get_all_ips(GITHUB_URLS, DNS_API_GOOGLE)

    logging.info("合并并去重两个 API 的 IP 地址")
    ips_merged = merge_deduplicate_ips(ips_cloudflare, ips_google)

    if not args.is_in_gha:
        logging.info("选择每个 URL 的最佳 IP 地址")
        ips_single = select_best_ip(ips_merged)

        logging.info("重新排序 IP 地址列表")
        ips_res = reorder_ips_with_best_first(ips_merged, ips_single)
    else:
        logging.info("在 GitHub Actions 环境中运行")
        # https://github.com/actions/runner-images/issues/1519#issuecomment-752644218
        # GitHub runners are placed in Azure. Ping doesn't work in azure by design.
        ips_single = select_first_ip(ips_merged)

        ips_res = ips_merged

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
