from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Retailer(Base):
    __tablename__ = "retailers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    retailer_id: Mapped[int] = mapped_column(ForeignKey("retailers.id"), nullable=False)
    store_number: Mapped[str | None] = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    address_line1: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(2), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(10), nullable=False)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    brand: Mapped[str | None] = mapped_column(String(150))
    upc_gtin: Mapped[str | None] = mapped_column(String(32), index=True)
    model_number: Mapped[str | None] = mapped_column(String(100), index=True)
    category: Mapped[str | None] = mapped_column(String(120), index=True)
    image_url: Mapped[str | None] = mapped_column(Text)


class StoreProduct(Base):
    __tablename__ = "store_products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    retailer_item_id: Mapped[str] = mapped_column(String(120), index=True)
    current_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    original_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    markdown_label: Mapped[str | None] = mapped_column(String(80))
    inventory_status: Mapped[str | None] = mapped_column(String(40))
    stock_level: Mapped[int | None] = mapped_column(Integer)
    pickup_available: Mapped[bool] = mapped_column(Boolean, default=False)
    shipping_available: Mapped[bool] = mapped_column(Boolean, default=False)
    quantity_text: Mapped[str | None] = mapped_column(String(120))
    product_url: Mapped[str | None] = mapped_column(Text)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    store_product_id: Mapped[int] = mapped_column(ForeignKey("store_products.id"), index=True)
    observed_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    observed_original_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    observed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class MarketplaceMatch(Base):
    __tablename__ = "marketplace_matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    store_product_id: Mapped[int] = mapped_column(ForeignKey("store_products.id"), index=True)
    marketplace: Mapped[str] = mapped_column(String(50), index=True)
    external_listing_id: Mapped[str | None] = mapped_column(String(120))
    estimated_sell_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    confidence: Mapped[Decimal] = mapped_column(Numeric(4, 3), default=0.0)
    match_factors: Mapped[dict] = mapped_column(JSON, default=dict)


class ResaleEstimate(Base):
    __tablename__ = "resale_estimates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    store_product_id: Mapped[int] = mapped_column(ForeignKey("store_products.id"), index=True)
    gross_profit: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    net_profit: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    roi_percent: Mapped[Decimal] = mapped_column(Numeric(8, 2))
    margin_percent: Mapped[Decimal] = mapped_column(Numeric(8, 2))
    risk_score: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    opportunity_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), index=True)
    confidence: Mapped[Decimal] = mapped_column(Numeric(4, 3), default=0.0)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(120))


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    retailer_code: Mapped[str | None] = mapped_column(String(32), index=True)
    store_id: Mapped[int | None] = mapped_column(ForeignKey("stores.id"), index=True)
    min_profit: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    min_roi: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    keyword: Mapped[str | None] = mapped_column(String(120))
    category: Mapped[str | None] = mapped_column(String(120))
    channel: Mapped[str] = mapped_column(String(20), default="email")
    destination: Mapped[str] = mapped_column(String(255), nullable=False)


class Watchlist(Base):
    __tablename__ = "watchlists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    store_product_id: Mapped[int] = mapped_column(ForeignKey("store_products.id"), index=True)
    notes: Mapped[str | None] = mapped_column(Text)
