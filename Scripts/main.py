"""Main script of the project."""

import argparse
import logging
from pathlib import Path

from constants import DNS_API_CLOUDFLARE, DNS_API_GOOGLE, GITHUB_URLS
from get_ip import get_all_ips
from process_ip import (
    format_host_strings,
    merge_deduplicate_ips,
    reorder_ips_with_best_first,
    select_best_ip,
    select_first_ip,
)
from update_readme import get_hosts_head_str, update_readme


def main():
    """Main function of the script."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    parser = argparse.ArgumentParser(description="GitHub IP hosts")
    parser.add_argument("--is_in_gha", type=bool, default=False, help="指定是否在GitHub Actions环境中运行")
    args = parser.parse_args()

    logging.info("通过Cloudflare DNS-over-HTTPS 获取GitHub的IP地址")
    ips_cloudflare = get_all_ips(GITHUB_URLS, DNS_API_CLOUDFLARE)

    logging.info("通过Google DNS-over-HTTPS 获取GitHub的IP地址")
    ips_google = get_all_ips(GITHUB_URLS, DNS_API_GOOGLE)

    logging.info("合并并去重两个API的IP地址")
    ips_merged = merge_deduplicate_ips(ips_cloudflare, ips_google)

    if not args.is_in_gha:
        logging.info("选择每个URL的最佳IP地址")
        ips_single = select_best_ip(ips_merged)

        logging.info("重新排序IP地址列表")
        ips_res = reorder_ips_with_best_first(ips_merged, ips_single)
    else:
        # https://github.com/actions/runner-images/issues/1519#issuecomment-752644218
        # GitHub runners are placed in Azure. Ping doesn't work in azure by design.
        ips_single = select_first_ip(ips_merged)

        ips_res = ips_merged

    logging.info("格式化hosts_single字符串")
    host_single_strings = format_host_strings(ips_single)

    logging.info("写入hosts_single文件")
    with open(Path("hosts_single"), "w", encoding="utf-8") as file:
        file.write(get_hosts_head_str("hosts_single") + host_single_strings + "\n\n# GitHub IP hosts End")

    logging.info("格式化host字符串")
    host_strings = format_host_strings(ips_res)

    logging.info("写入hosts文件")
    host_content = get_hosts_head_str("hosts") + host_strings + "\n\n# GitHub IP hosts End"
    with open(Path("hosts"), "w", encoding="utf-8") as file:
        file.write(host_content)

    print(host_content)

    logging.info("更新README.md")
    update_readme("```\n" + host_content + "\n```")


if __name__ == "__main__":
    main()
