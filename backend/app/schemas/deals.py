from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class DealView(BaseModel):
    retailer_name: str
    store_location: str
    store_number: str | None = None
    product_title: str
    brand: str | None = None
    sku_item_id: str
    upc_gtin: str | None = None
    current_price: Decimal
    original_price: Decimal | None = None
    discount_percent: float = Field(default=0.0)
    clearance_label: str | None = None
    stock_level: int | None = None
    deal_confidence: float = Field(default=0.0)
    product_url: str | None = None
    image_url: str | None = None
    estimated_resale_profit: Decimal
    estimated_roi: Decimal
    updated_at: datetime


class DealQuery(BaseModel):
    retailer_codes: list[str] = []
    zip_code: str | None = None
    radius_miles: int = 25
    store_ids: list[int] = []
    min_profit: float | None = None
    min_roi: float | None = None
    clearance_only: bool = False
    sort_by: str = "highest_roi"
