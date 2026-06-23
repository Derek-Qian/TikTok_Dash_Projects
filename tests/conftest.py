from __future__ import annotations

import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

TEST_DATABASE_URL = "sqlite+aiosqlite://"

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS tk_fill_batches (
    batch_id VARCHAR(64) PRIMARY KEY,
    task_name VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tk_fill_products (
    product_id VARCHAR(64) PRIMARY KEY,
    batch_id VARCHAR(64) NOT NULL,
    product_title VARCHAR(255),
    category_id VARCHAR(64),
    brand_id VARCHAR(64),
    status VARCHAR(20) DEFAULT 'pending',
    tiktok_product_id VARCHAR(64),
    last_sync_error TEXT,
    base_data TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    update_time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS tk_fill_product_skus (
    sku_id VARCHAR(64) PRIMARY KEY,
    batch_id VARCHAR(64) NOT NULL,
    product_id VARCHAR(64) NOT NULL,
    sku_attributes TEXT,
    sku_image_uri TEXT,
    parcel_weight NUMERIC,
    parcel_length NUMERIC,
    parcel_width NUMERIC,
    parcel_height NUMERIC,
    price NUMERIC,
    warehouse_quantity INTEGER,
    seller_sku VARCHAR(255),
    sku_data TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    update_time TIMESTAMP NOT NULL
);
"""


@pytest_asyncio.fixture
async def async_engine_test():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        for stmt in CREATE_TABLES_SQL.split(";"):
            stmt = stmt.strip()
            if stmt:
                await conn.execute(text(stmt))
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(async_engine_test) -> AsyncSession:
    from sqlalchemy.ext.asyncio import async_sessionmaker

    factory = async_sessionmaker(bind=async_engine_test, expire_on_commit=False)
    async with factory() as s:
        yield s
