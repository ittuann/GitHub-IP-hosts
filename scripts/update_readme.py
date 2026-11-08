"""Update the status part in README.md file.

Update the README.md file with the current status of hosts.

Note:
    File   : update_readme.py
    Author : ittuann <ittuann@outlook.com> (https://github.com/ittuann)
    License: Apache-2.0 License.
"""

import re
from datetime import datetime, timedelta, timezone

from scripts.constants import PROJECT_ROOT

HOSTS_START_MARK = "<!-- hosts-all-start -->"
HOSTS_END_MARK = "<!-- hosts-all-end -->"


def update_readme(hosts_content: str) -> None:
    """更新README.md文件中的 hosts 部分。

    Parameters:
        hosts_content (str): 要更新的状态字符串。

    Raises:
        ValueError: README.md 中找不到 hosts 标记。
    """
    readme_path = PROJECT_ROOT / "README.md"

    with open(readme_path, encoding="utf-8") as file:
        md_content = file.read()

    # 通过正则表达式找到并替换 hosts 部分
    replacement = f"{HOSTS_START_MARK}\n\n{hosts_content}\n\n{HOSTS_END_MARK}"
    new_content, count = re.subn(
        rf"{re.escape(HOSTS_START_MARK)}.*?{re.escape(HOSTS_END_MARK)}",
        lambda _: replacement,
        md_content,
        count=1,
        flags=re.DOTALL,
    )
    if count == 0:
        raise ValueError(f"{readme_path} 中找不到 {HOSTS_START_MARK} 和 {HOSTS_END_MARK} 标记")

    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(new_content)


def get_time_str() -> str:
    """获取当前时间的字符串表示形式。

    Returns:
        str: 当前时间的字符串表示形式。
    """
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    date_str = now.strftime("%Y-%m-%d %H:%M:%S %Z")
    return date_str


def get_hosts_head_str() -> str:
    """获取hosts文件的头部字符串。

    Returns:
        str: hosts文件的头部字符串。
    """
    return f"""# GitHub IP hosts Start
# Auto update time: {get_time_str()}
# IP 可能会随时变化，为确保不错过重要更新，请前往 GitHub 项目页面 Star 这个仓库，以及时获取最新数据和信息
# GitHub URL: https://github.com/ittuann/GitHub-IP-hosts

"""
