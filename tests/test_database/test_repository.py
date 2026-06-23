from __future__ import annotations

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repository import upsert_batch, upsert_product


@pytest.mark.asyncio
async def test_upsert_batch(session: AsyncSession) -> None:
    """测试批次记录幂等写入"""
    await upsert_batch(session, "test-batch-001", "test-task")
    result = await session.execute(
        text("SELECT batch_id, task_name FROM tk_fill_batches WHERE batch_id = :bid"),
        {"bid": "test-batch-001"},
    )
    row = result.fetchone()
    assert row is not None
    assert row[0] == "test-batch-001"
    assert row[1] == "test-task"


@pytest.mark.asyncio
async def test_upsert_product(session: AsyncSession) -> None:
    """测试商品幂等写入"""
    await upsert_product(session, "p001", "batch-1", "测试商品", '{"key": "val"}')
    result = await session.execute(
        text("SELECT product_id, product_title FROM tk_fill_products WHERE product_id = :pid"),
        {"pid": "p001"},
    )
    row = result.fetchone()
    assert row is not None
    assert row[0] == "p001"
    assert row[1] == "测试商品"
