"""Update the status part in README.md file."""

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path


def update_readme(status: str) -> None:
    """更新README.md文件中的状态部分。

    Parameters:
        status (str): 要更新的状态字符串。
    """
    readme_path = Path("README.md")

    with open(readme_path, encoding="utf-8") as file:
        content = file.read()

    # 通过正则表达式找到并替换状态部分
    new_content = re.sub(
        r"<!-- hosts-all-start -->.*<!-- hosts-all-end -->",
        f"<!-- hosts-all-start -->\n\n{status}\n\n<!-- hosts-all-end -->",
        content,
        flags=re.DOTALL,
    )

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


def get_hosts_head_str(hosts_name: str) -> str:
    """获取hosts文件的头部字符串。

    Parameters:
        hosts_name (str): hosts文件的名称。

    Returns:
        str: hosts文件的头部字符串。
    """
    return f"""# GitHub IP hosts Start
# Auto update time: {get_time_str()}
# IP可能会随时变化，请关注GitHub项目，以获取最新数据
# GitHub  url: https://github.com/ittuann/GitHub-IP-hosts
# Update  url: https://github.com/ittuann/GitHub-IP-hosts/{hosts_name}

"""
