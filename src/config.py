from __future__ import annotations

import os
from dataclasses import dataclass, field
from urllib.parse import quote

from dotenv import load_dotenv

load_dotenv(override=True)


@dataclass(frozen=True)
class Config:
    # --- Apify ---
    APIFY_TOKEN: str = field(default_factory=lambda: os.getenv("APIFY_TOKEN", ""))

    # --- PostgreSQL ---
    DB_NAME: str = field(default_factory=lambda: os.getenv("DB_NAME", ""))
    DB_USER: str = field(default_factory=lambda: os.getenv("DB_USER", ""))
    DB_PASSWORD: str = field(default_factory=lambda: os.getenv("DB_PASSWORD", ""))
    DB_HOST: str = field(default_factory=lambda: os.getenv("DB_HOST", "127.0.0.1"))
    DB_PORT: str = field(default_factory=lambda: os.getenv("DB_PORT", "5432"))

    @property
    def db_dsn(self) -> str:
        """异步 SQLAlchemy DSN（密码中的特殊字符已 URL 编码）"""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{quote(self.DB_PASSWORD, safe='')}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # --- TikTok Shop API ---
    TIKTOK_APP_KEY: str = field(default_factory=lambda: os.getenv("TIKTOK_APP_KEY", ""))
    TIKTOK_APP_SECRET: str = field(default_factory=lambda: os.getenv("TIKTOK_APP_SECRET", ""))
    TIKTOK_ACCESS_TOKEN: str = field(default_factory=lambda: os.getenv("TIKTOK_ACCESS_TOKEN", ""))
    TIKTOK_SHOP_ID: str = field(default_factory=lambda: os.getenv("TIKTOK_SHOP_ID", ""))
    TIKTOK_SHOP_CIPHER: str = field(default_factory=lambda: os.getenv("TIKTOK_SHOP_CIPHER", ""))
    TIKTOK_WAREHOUSE_ID: str = field(default_factory=lambda: os.getenv("TIKTOK_WAREHOUSE_ID", ""))
    TIKTOK_API_BASE: str = "https://open-api.tiktokglobalshop.com"

    # --- 业务参数 ---
    DAILY_OFFER_IDS: list[str] = field(
        default_factory=lambda: [
            "765357586765",
            "657494702049",
            "792416878138",
            "783518415985",
            "668031060778",
        ]
    )
    APIFY_ACTOR_ID: str = "zen-studio/1688-wholesale-scraper"


config = Config()
