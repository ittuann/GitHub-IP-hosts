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
    # "actions.githubusercontent.com",
    "avatars.githubusercontent.com",
    "avatars0.githubusercontent.com",
    "avatars1.githubusercontent.com",
    "avatars2.githubusercontent.com",
    "avatars3.githubusercontent.com",
    "avatars4.githubusercontent.com",
    "avatars5.githubusercontent.com",
    "broker.actions.githubusercontent.com",
    "camo.githubusercontent.com",
    "central.github.com",
    "cloud.githubusercontent.com",
    "codeload.github.com",
    "collector.github.com",
    "containers.pkg.github.com",
    "copilot-proxy.githubusercontent.com",
    "desktop.githubusercontent.com",
    "dependabot-actions.githubapp.com",
    "default.exp-tas.com",
    "docker.pkg.github.com",
    "docker-proxy.pkg.github.com",
    "education.github.com",
    "favicons.githubusercontent.com",
    "fulcio.githubapp.com",
    "ghcr.io",
    "gist.github.com",
    "github-cloud.s3.amazonaws.com",
    "github-com.s3.amazonaws.com",
    "github.blog",
    "github.com",
    "github.community",
    "github.dev",
    "github.global.ssl.fastly.net",
    "github.io",
    "github.map.fastly.net",
    # "githubassets.com",
    "githubcopilot.com",
    # "githubusercontent.com",
    "githubstatus.com",
    "github-cloud.githubusercontent.com",
    "github-cloud.s3.amazonaws.com",
    "github-releases.githubusercontent.com",
    "github-registry-files.githubusercontent.com",
    "launch.actions.githubusercontent.com",
    "live.github.com",
    "maven.pkg.github.com",
    "media.githubusercontent.com",
    # "msecnd.net",
    "mpsghub.actions.githubusercontent.com",
    "npm.pkg.github.com",
    "npm-proxy.pkg.github.com",
    "npm-beta-proxy.pkg.github.com",
    "npm-beta.pkg.github.com",
    "npmregistryv2prod.blob.core.windows.net",
    "nuget.pkg.github.com",
    "objects.githubusercontent.com",
    "objects-origin.githubusercontent.com",
    "origin-tracker.githubusercontent.com",
    "pipelines.actions.githubusercontent.com",
    "pipelinesghubeus1.actions.githubusercontent.com",
    "pkg.github.com",
    "pkg.actions.githubusercontent.com",
    "pkg-containers.githubusercontent.com",
    "productionresultssa1.blob.core.windows.net",
    "pypi.pkg.github.com",
    "raw.githubusercontent.com",
    "release-assets.githubusercontent.com",
    "results-receiver.actions.githubusercontent.com",
    "rubygems.pkg.github.com",
    "runnerghubeus1.actions.githubusercontent.com",
    "run-actions-1-azure-eastus.actions.githubusercontent.com",
    "runner-auth.actions.githubusercontent.com",
    "setup-tools.actions.githubusercontent.com",
    "swift.pkg.github.com",
    "timestamp.githubapp.com",
    "tokenghub.actions.githubusercontent.com",
    "tuf-repo.github.com",
    "user-images.githubusercontent.com",
    "visualstudio.com",
    # "vscode-webview.net",
    "vstoken.actions.githubusercontent.com",
]
