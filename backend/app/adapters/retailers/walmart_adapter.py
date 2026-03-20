from datetime import datetime

import httpx

from app.adapters.retailers.base import NormalizedRetailDeal, RetailerAdapter


class WalmartRetailerAdapter(RetailerAdapter):
    """Example adapter stub. Replace endpoint mapping with official API integration."""

    code = "walmart"

    def __init__(self, base_url: str = "https://developer.api.walmart.com") -> None:
        self.base_url = base_url

    async def fetch_store_deals(self, *, zip_code: str, radius_miles: int, store_ids: list[str] | None = None) -> list[NormalizedRetailDeal]:
        params = {"zipCode": zip_code, "radius": radius_miles}
        timeout = httpx.Timeout(15.0)

        async with httpx.AsyncClient(timeout=timeout) as client:
            # Placeholder call to illustrate API pattern.
            await client.get(f"{self.base_url}/api-proxy/service/affil/product/v2/search", params=params)

        return [
            NormalizedRetailDeal(
                retailer_code=self.code,
                store_id=store_ids[0] if store_ids else "demo-store",
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
