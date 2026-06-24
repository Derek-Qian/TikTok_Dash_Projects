"""数据库迁移：为 tk_fill_products 增加价格相关字段"""
from __future__ import annotations

import asyncio

from sqlalchemy import text

from src.database.engine import create_session


async def migrate() -> None:
    """增加 original_price、source_region、suggested_price 等字段"""
    async with create_session() as session:
        await session.execute(
            text("""
                ALTER TABLE tk_fill_products
                ADD COLUMN IF NOT EXISTS original_price NUMERIC(12, 2),
                ADD COLUMN IF NOT EXISTS suggested_price NUMERIC(12, 2),
                ADD COLUMN IF NOT EXISTS target_region VARCHAR(10)
            """)
        )
        await session.commit()
        print("✅ 价格字段迁移完成")


if __name__ == "__main__":
    asyncio.run(migrate())
