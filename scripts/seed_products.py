"""
手动触发一次 1688 数据采集并写入数据库
用法: uv run python scripts/seed_products.py
"""

from __future__ import annotations

import asyncio
import logging

from src.database.engine import create_session
from src.services.sync_service import SyncService

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    print("🚀 开始手动同步 1688 数据...")
    service = SyncService()

    async with create_session() as session:
        result = await service.run(session)

    print(f"📊 同步结果: {result}")
    print("✅ 同步完成")


if __name__ == "__main__":
    asyncio.run(main())
