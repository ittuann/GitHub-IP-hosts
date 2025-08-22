"""Code Coverage Test.

Note:
    File   : test_functions.py
    Author : ittuann <ittuann@outlook.com> (https://github.com/ittuann)
    License: Apache-2.0 License.
"""

from scripts.constants import DNS_API_CLOUDFLARE, DNS_API_GOOGLE, GITHUB_URLS
from scripts.get_ip import DNSRecord, URLIPMapping


def test_dnsrecord_class():
    """Test DNSRecord class."""
    record = DNSRecord(name="example.com", type=1, TTL=300, data="1.2.3.4")
    assert record.name == "example.com"
    assert record.type == 1
    assert record.ttl == 300
    assert record.data == "1.2.3.4"


def test_urlipmapping_class():
    """Test URLIPMapping class."""
    mapping = URLIPMapping(url="example.com", ip="1.2.3.4")
    assert mapping.url == "example.com"
    assert mapping.ip == "1.2.3.4"
    assert mapping.to_dict() == {"example.com": "1.2.3.4"}
    assert str(mapping) == "URLIPMapping(url='example.com', ip='1.2.3.4')"


def test_constants():
    """Test constants"""
    assert isinstance(DNS_API_GOOGLE, str)
    assert isinstance(DNS_API_CLOUDFLARE, str)
    assert isinstance(GITHUB_URLS, list)
    assert all(isinstance(url, str) for url in GITHUB_URLS)
