from __future__ import annotations

from typing import Any


class TikTokProductRequest:
    """TikTok CreateProduct 请求结构（简化）"""

    def __init__(self, raw_1688: dict[str, Any]) -> None:
        self.external_id: str = str(raw_1688.get("offerId", ""))
        self.title: str = raw_1688.get("title") or ""
        self.description: str = raw_1688.get("description") or ""
        self.images: list[str] = raw_1688.get("images") or []

    def to_dict(self) -> dict[str, Any]:
        return {
            "external_product_id": self.external_id,
            "product_name": self.title,
            "description": self.description,
            "main_images": self.images,
        }
