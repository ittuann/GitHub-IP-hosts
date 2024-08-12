# 📄 GitHub IP hosts

[![GitHub Action][ci-image]][ci-url]

[ci-image]: https://img.shields.io/github/actions/workflow/status/ittuann/GitHub-IP-hosts/workflow.yml?branch=main&label=Build%20Status&logo=github&style=for-the-badge
[ci-url]: https://github.com/ittuann/GitHub-IP-hosts/actions

通过使用 GitHub Action 每周自动更新 hosts 文件，解决中国大陆访问 GitHub 时遇到的抽风问题，诸如访问缓慢、图片加载失败等等。

# 目录

- [🛠️ 使用方法](#️-使用方法)
  - [1. 复制下面的 hosts 内容](#1-复制下面的-hosts-内容)
  - [2. 将内容粘贴到系统 hosts 文件中](#2-将内容粘贴到系统-hosts-文件中)
    - [Windows 系统粘贴](#windows-系统粘贴)
    - [Linux 系统粘贴](#linux-系统粘贴)
- [🔭 进阶使用](#-进阶使用)
  - 只记录单一 IP 的 [hosts](https://github.com/ittuann/GitHub-IP-hosts/blob/main/hosts_single) 文件
  - 在本地/海外服务器自部署
  - 默认返回所有响应中速度最快的 IP 地址

# 🛠️ 使用方法

使用方法仅需 2 步: 复制 [hosts](https://github.com/ittuann/GitHub-IP-hosts/blob/main/hosts) 文本 -> 将复制的文本粘贴至系统 hosts 文件

## 1. 复制下面的 hosts 内容

<!-- hosts-all-start -->

```
# GitHub IP hosts Start
# Auto update time: 2024-08-12 13:02:28 UTC+08:00
# IP 可能会随时变化，请关注 GitHub 项目，以获取最新数据
# GitHub url: https://github.com/ittuann/GitHub-IP-hosts
# Update url: https://raw.githubusercontent.com/ittuann/GitHub-IP-hosts/main/hosts

140.82.112.25   alive.github.com
140.82.113.25   alive.github.com
140.82.112.5    api.github.com
140.82.114.6    api.github.com
185.199.108.153 assets-cdn.github.com
185.199.109.153 assets-cdn.github.com
185.199.110.153 assets-cdn.github.com
185.199.111.153 assets-cdn.github.com
185.199.108.133 avatars.githubusercontent.com
185.199.109.133 avatars.githubusercontent.com
185.199.110.133 avatars.githubusercontent.com
185.199.111.133 avatars.githubusercontent.com
185.199.108.133 avatars0.githubusercontent.com
185.199.109.133 avatars0.githubusercontent.com
185.199.110.133 avatars0.githubusercontent.com
185.199.111.133 avatars0.githubusercontent.com
185.199.108.133 avatars1.githubusercontent.com
185.199.109.133 avatars1.githubusercontent.com
185.199.110.133 avatars1.githubusercontent.com
185.199.111.133 avatars1.githubusercontent.com
185.199.108.133 avatars2.githubusercontent.com
185.199.109.133 avatars2.githubusercontent.com
185.199.110.133 avatars2.githubusercontent.com
185.199.111.133 avatars2.githubusercontent.com
185.199.108.133 avatars3.githubusercontent.com
185.199.109.133 avatars3.githubusercontent.com
185.199.110.133 avatars3.githubusercontent.com
185.199.111.133 avatars3.githubusercontent.com
185.199.108.133 avatars4.githubusercontent.com
185.199.109.133 avatars4.githubusercontent.com
185.199.110.133 avatars4.githubusercontent.com
185.199.111.133 avatars4.githubusercontent.com
185.199.108.133 avatars5.githubusercontent.com
185.199.109.133 avatars5.githubusercontent.com
185.199.110.133 avatars5.githubusercontent.com
185.199.111.133 avatars5.githubusercontent.com
185.199.108.133 camo.githubusercontent.com
185.199.109.133 camo.githubusercontent.com
185.199.110.133 camo.githubusercontent.com
185.199.111.133 camo.githubusercontent.com
140.82.113.22   central.github.com
140.82.114.22   central.github.com
185.199.108.133 cloud.githubusercontent.com
185.199.109.133 cloud.githubusercontent.com
185.199.110.133 cloud.githubusercontent.com
185.199.111.133 cloud.githubusercontent.com
140.82.112.9    codeload.github.com
140.82.112.22   collector.github.com
140.82.114.21   collector.github.com
185.199.108.133 desktop.githubusercontent.com
185.199.109.133 desktop.githubusercontent.com
185.199.110.133 desktop.githubusercontent.com
185.199.111.133 desktop.githubusercontent.com
140.82.112.22   education.github.com
140.82.113.21   education.github.com
185.199.108.133 favicons.githubusercontent.com
185.199.109.133 favicons.githubusercontent.com
185.199.110.133 favicons.githubusercontent.com
185.199.111.133 favicons.githubusercontent.com
140.82.112.4    gist.github.com
140.82.113.4    gist.github.com
16.182.100.17   github-cloud.s3.amazonaws.com
16.182.106.241  github-cloud.s3.amazonaws.com
3.5.25.102      github-cloud.s3.amazonaws.com
3.5.25.30       github-cloud.s3.amazonaws.com
16.182.100.17   github-com.s3.amazonaws.com
16.182.106.241  github-com.s3.amazonaws.com
16.182.68.1     github-com.s3.amazonaws.com
3.5.27.116      github-com.s3.amazonaws.com
192.0.66.2      github.blog
140.82.113.4    github.com
140.82.114.4    github.com
140.82.113.17   github.community
140.82.113.18   github.community
185.199.108.154 github.githubassets.com
185.199.109.154 github.githubassets.com
185.199.110.154 github.githubassets.com
185.199.111.154 github.githubassets.com
151.101.1.194   github.global.ssl.fastly.net
151.101.129.194 github.global.ssl.fastly.net
151.101.193.194 github.global.ssl.fastly.net
151.101.65.194  github.global.ssl.fastly.net
185.199.108.153 github.io
185.199.109.153 github.io
185.199.110.153 github.io
185.199.111.153 github.io
185.199.108.133 github.map.fastly.net
185.199.109.133 github.map.fastly.net
185.199.110.133 github.map.fastly.net
185.199.111.133 github.map.fastly.net
185.199.108.153 githubstatus.com
185.199.109.153 githubstatus.com
185.199.110.153 githubstatus.com
185.199.111.153 githubstatus.com
140.82.112.25   live.github.com
140.82.113.25   live.github.com
185.199.108.133 media.githubusercontent.com
185.199.109.133 media.githubusercontent.com
185.199.110.133 media.githubusercontent.com
185.199.111.133 media.githubusercontent.com
185.199.108.133 objects.githubusercontent.com
185.199.109.133 objects.githubusercontent.com
185.199.110.133 objects.githubusercontent.com
185.199.111.133 objects.githubusercontent.com
13.107.42.16    pipelines.actions.githubusercontent.com
185.199.108.133 raw.githubusercontent.com
185.199.109.133 raw.githubusercontent.com
185.199.110.133 raw.githubusercontent.com
185.199.111.133 raw.githubusercontent.com
185.199.108.133 user-images.githubusercontent.com
185.199.109.133 user-images.githubusercontent.com
185.199.110.133 user-images.githubusercontent.com
185.199.111.133 user-images.githubusercontent.com

# GitHub IP hosts End

```

<!-- hosts-all-end -->

## 2. 将内容粘贴到系统 hosts 文件中

### Windows 系统粘贴

1. 在搜索框中输入`记事本`，右键选择`以管理员身份运行`打开记事本。
2. 在记事本中依次点击`文件` -> `打开`
3. 将弹出框右下角的文件类型从`文本文档(*.txt)`改为`所有文件(*.*)`
4. 前往路径: `C:\Windows\System32\drivers\etc`，然后选择`hosts`文件即可开始编辑
5. 将复制的内容直接粘贴到文件末尾，保存即可

大部分情况下无需手动刷新 DNS，如未生效可在 CMD / PowerShell 中执行`ipconfig /flushdns`

### Linux 系统粘贴

在终端中执行 `sudoedit /etc/hosts`，然后将复制的内容直接粘贴到文件末尾，保存即可。

# 🔭 进阶使用

1. 项目默认支持返回所有响应中速度最快的 IP 地址。
2. 使用只记录单一 IP 的 hosts 文件: 复制项目内的 [hosts_single](https://github.com/ittuann/GitHub-IP-hosts/blob/main/hosts_single) 文件内容即可。
3. 在本地/海外服务器自部署项目: 在项目根目录使用终端执行 `make` 命令即可。
4. 通过 [SwitchHosts](https://github.com/oldj/SwitchHosts) 工具自动更新 hosts 文件。
5. 完整的 workflows 工作流请参考 [GitHub Action](https://github.com/ittuann/GitHub-IP-hosts/actions) 的 CI/CD 配置。
