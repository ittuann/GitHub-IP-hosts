"""Constants for the GitHub API.

This module contains constants used for interacting with the GitHub API and DNS-over-HTTPS APIs.

Constants:
    DNS_API_CLOUDFLARE (str): URL for Cloudflare DNS-over-HTTPS API.
    DNS_API_GOOGLE (str): URL for Google DNS-over-HTTPS API.
    GITHUB_URLS (List[str]): List of GitHub-related URLs.

Note:
    File   : constants.py
    Author : ittuann <ittuann@outlook.com> (https://github.com/ittuann)
    License: Apache-2.0 License.
"""

# Cloudflare DNS-over-HTTPS API
DNS_API_CLOUDFLARE: str = "https://cloudflare-dns.com/dns-query"

# Google DNS-over-HTTPS API
DNS_API_GOOGLE: str = "https://dns.google/resolve"

GITHUB_URLS: list[str] = [
    "alive.github.com",
    "api.github.com",
    "avatars.githubusercontent.com",
    "avatars0.githubusercontent.com",
    "avatars1.githubusercontent.com",
    "avatars2.githubusercontent.com",
    "avatars3.githubusercontent.com",
    "avatars4.githubusercontent.com",
    "avatars5.githubusercontent.com",
    "camo.githubusercontent.com",
    "central.github.com",
    "cloud.githubusercontent.com",
    "codeload.github.com",
    "collector.github.com",
    "copilot-proxy.githubusercontent.com",
    "desktop.githubusercontent.com",
    "favicons.githubusercontent.com",
    "gist.github.com",
    "github-cloud.s3.amazonaws.com",
    "github-com.s3.amazonaws.com",
    "github.blog",
    "github.com",
    "github.community",
    "github.githubassets.com",
    "github.global.ssl.fastly.net",
    "github.io",
    "github.map.fastly.net",
    "githubcopilot.com",
    "githubstatus.com",
    "live.github.com",
    "media.githubusercontent.com",
    "objects.githubusercontent.com",
    "origin-tracker.githubusercontent.com",
    "pipelines.actions.githubusercontent.com",
    "raw.githubusercontent.com",
    "user-images.githubusercontent.com",
    "education.github.com",
]
