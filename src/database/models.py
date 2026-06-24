from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TkFillBatch(Base):
    __tablename__ = "tk_fill_batches"

    batch_id: Mapped[str] = mapped_column(primary_key=True)
    task_name: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False))


class TkFillProduct(Base):
    __tablename__ = "tk_fill_products"

    product_id: Mapped[str] = mapped_column(primary_key=True)
    batch_id: Mapped[str] = mapped_column()
    product_title: Mapped[str | None] = mapped_column()
    category_id: Mapped[str | None] = mapped_column()
    brand_id: Mapped[str | None] = mapped_column()
    status: Mapped[str | None] = mapped_column()
    tiktok_product_id: Mapped[str | None] = mapped_column()
    last_sync_error: Mapped[str | None] = mapped_column(Text)
    base_data: Mapped[str] = mapped_column()
    original_price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    suggested_price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    target_region: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    update_time: Mapped[datetime] = mapped_column(DateTime(timezone=False))


class TkFillProductSku(Base):
    __tablename__ = "tk_fill_product_skus"

    sku_id: Mapped[str] = mapped_column(primary_key=True)
    batch_id: Mapped[str] = mapped_column()
    product_id: Mapped[str] = mapped_column()
    sku_attributes: Mapped[str | None] = mapped_column()
    sku_image_uri: Mapped[str | None] = mapped_column(Text)
    parcel_weight: Mapped[float | None] = mapped_column(Numeric)
    parcel_length: Mapped[float | None] = mapped_column(Numeric)
    parcel_width: Mapped[float | None] = mapped_column(Numeric)
    parcel_height: Mapped[float | None] = mapped_column(Numeric)
    price: Mapped[float | None] = mapped_column(Numeric)
    warehouse_quantity: Mapped[int | None] = mapped_column(Integer)
    seller_sku: Mapped[str | None] = mapped_column()
    sku_data: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    update_time: Mapped[datetime] = mapped_column(DateTime(timezone=False))


class TkShop(Base):
    __tablename__ = "tk_shops"

    shop_id: Mapped[str] = mapped_column(primary_key=True)
    shop_name: Mapped[str | None] = mapped_column()
    region: Mapped[str | None] = mapped_column()
    shop_cipher: Mapped[str | None] = mapped_column(Text)
    seller_type: Mapped[str | None] = mapped_column()
    app_key: Mapped[str | None] = mapped_column()
    update_time: Mapped[datetime] = mapped_column(DateTime(timezone=False))


class TkAuthInfo(Base):
    __tablename__ = "tk_auth_info"

    app_key: Mapped[str] = mapped_column(primary_key=True)
    app_secret: Mapped[str | None] = mapped_column()
    access_token: Mapped[str | None] = mapped_column(Text)
    refresh_token: Mapped[str | None] = mapped_column(Text)
    access_token_expires_at: Mapped[int | None] = mapped_column()
    refresh_token_expires_at: Mapped[int | None] = mapped_column()
    seller_name: Mapped[str | None] = mapped_column()
    open_id: Mapped[str | None] = mapped_column(Text)
    request_id: Mapped[str | None] = mapped_column(Text)
    update_time: Mapped[datetime | None] = mapped_column()


class TkWarehouse(Base):
    __tablename__ = "tk_warehouses"

    warehouse_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column()
    effect_status: Mapped[str | None] = mapped_column()
    type: Mapped[str | None] = mapped_column()
    sub_type: Mapped[str | None] = mapped_column()
    is_default: Mapped[bool | None] = mapped_column()
    entity_id: Mapped[str | None] = mapped_column()
    address_data: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False))
