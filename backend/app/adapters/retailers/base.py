from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class NormalizedRetailDeal:
    retailer_code: str
    store_id: str
    store_number: str | None
    item_id: str
    title: str
    brand: str | None
    upc: str | None
    current_price: float
    original_price: float | None
    stock_level: int | None
    inventory_status: str | None
    markdown_label: str | None
    product_url: str | None
    image_url: str | None
    category: str | None
    fetched_at: datetime


class RetailerAdapter(ABC):
    code: str

    @abstractmethod
    async def fetch_store_deals(self, *, zip_code: str, radius_miles: int, store_ids: list[str] | None = None) -> list[NormalizedRetailDeal]:
        """Fetch store-scoped deals with compliance-safe rate limiting and retries."""
        raise NotImplementedError
