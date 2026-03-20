from datetime import datetime

from app.adapters.retailers.walmart_adapter import WalmartRetailerAdapter
from app.schemas.deals import DealQuery, DealView


class DealService:
    def __init__(self) -> None:
        self.walmart_adapter = WalmartRetailerAdapter()

    async def get_all_store_deals(self, query: DealQuery) -> list[DealView]:
        deals = await self.walmart_adapter.fetch_store_deals(
            zip_code=query.zip_code or "10001",
            radius_miles=query.radius_miles,
            store_ids=[str(s) for s in query.store_ids] if query.store_ids else None,
        )

        response: list[DealView] = []
        for deal in deals:
            original = deal.original_price or deal.current_price
            discount_percent = ((original - deal.current_price) / original * 100) if original else 0
            est_profit = round((deal.current_price * 0.85), 2)
            est_roi = round((est_profit / deal.current_price) * 100, 2) if deal.current_price else 0
            response.append(
                DealView(
                    retailer_name=deal.retailer_code.title(),
                    store_location=f"Store {deal.store_number or deal.store_id}",
                    store_number=deal.store_number,
                    product_title=deal.title,
                    brand=deal.brand,
                    sku_item_id=deal.item_id,
                    upc_gtin=deal.upc,
                    current_price=deal.current_price,
                    original_price=deal.original_price,
                    discount_percent=round(discount_percent, 2),
                    clearance_label=deal.markdown_label,
                    stock_level=deal.stock_level,
                    deal_confidence=0.78,
                    product_url=deal.product_url,
                    image_url=deal.image_url,
                    estimated_resale_profit=est_profit,
                    estimated_roi=est_roi,
                    updated_at=datetime.utcnow(),
                )
            )

        return response
