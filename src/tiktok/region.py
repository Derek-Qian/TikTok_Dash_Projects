from __future__ import annotations

_REGION_MAP: dict[str, dict[str, str]] = {
    "MY": {"locale": "ms-MY", "currency": "MYR", "name": "马来西亚"},
    "VN": {"locale": "vi-VN", "currency": "VND", "name": "越南"},
    "TH": {"locale": "th-TH", "currency": "THB", "name": "泰国"},
    "PH": {"locale": "en-PH", "currency": "PHP", "name": "菲律宾"},
    "ID": {"locale": "id-ID", "currency": "IDR", "name": "印尼"},
    "SG": {"locale": "en-SG", "currency": "SGD", "name": "新加坡"},
    "US": {"locale": "en-US", "currency": "USD", "name": "美国"},
    "GB": {"locale": "en-GB", "currency": "GBP", "name": "英国"},
}


def get_region_info(region: str) -> dict[str, str]:
    return _REGION_MAP.get(region.upper(), {"locale": "en-US", "currency": "USD", "name": region})
