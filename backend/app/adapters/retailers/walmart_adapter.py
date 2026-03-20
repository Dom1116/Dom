from datetime import datetime

from app.adapters.retailers.base import NormalizedRetailDeal, RetailerAdapter


class WalmartRetailerAdapter(RetailerAdapter):
    """Reference adapter shape for future Walmart API integration."""

    code = "walmart"

    async def fetch_store_deals(self, *, zip_code: str, radius_miles: int, store_ids: list[str] | None = None) -> list[NormalizedRetailDeal]:
        return [
            NormalizedRetailDeal(
                retailer_code=self.code,
                store_id=store_ids[0] if store_ids else "wm-1001",
                store_number="1001",
                item_id="WM-123",
                title="Walmart Demo Drill Set",
                brand="HyperTough",
                upc="012345678901",
                current_price=49.00,
                original_price=89.00,
                stock_level=8,
                inventory_status="in_stock",
                markdown_label="Clearance",
                product_url="https://www.walmart.com/ip/demo",
                image_url="https://i5.walmartimages.com/asr/demo.jpeg",
                category="Tools",
                fetched_at=datetime.utcnow(),
            )
        ]
