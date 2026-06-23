"""
初始化数据库表结构
用法: uv run python scripts/init_db.py
"""

from __future__ import annotations

import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

from src.config import config
from src.database.models import Base


async def main() -> None:
    print("🚀 正在创建数据库表...")
    engine = create_async_engine(config.db_dsn, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ 所有表已创建完成")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
