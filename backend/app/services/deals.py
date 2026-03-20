from datetime import datetime

from app.adapters.retailers.sample_adapters import build_personal_adapters
from app.schemas.deals import DealQuery, DealView


class DealService:
    def __init__(self) -> None:
        self.adapters = build_personal_adapters()

    async def get_all_store_deals(self, query: DealQuery) -> list[DealView]:
        selected_retailers = query.retailer_codes or list(self.adapters.keys())

        normalized = []
        for retailer_code in selected_retailers:
            adapter = self.adapters.get(retailer_code)
            if not adapter:
                continue
            normalized.extend(
                await adapter.fetch_store_deals(
                    zip_code=query.zip_code or "00000",
                    radius_miles=query.radius_miles,
                    store_ids=query.store_ids or None,
                )
            )

        mapped: list[DealView] = []
        for deal in normalized:
            original = deal.original_price or deal.current_price
            discount_percent = ((original - deal.current_price) / original * 100) if original else 0
            est_profit = round((deal.current_price * 0.45), 2)
            est_roi = round((est_profit / deal.current_price) * 100, 2) if deal.current_price else 0

            if query.clearance_only and not deal.markdown_label:
                continue
            if query.min_profit is not None and est_profit < query.min_profit:
                continue
            if query.min_roi is not None and est_roi < query.min_roi:
                continue

            mapped.append(
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
                    deal_confidence=0.80,
                    product_url=deal.product_url,
                    image_url=deal.image_url,
                    estimated_resale_profit=est_profit,
                    estimated_roi=est_roi,
                    updated_at=datetime.utcnow(),
                )
            )

        return sorted(mapped, key=lambda row: self._sort_key(row, query.sort_by), reverse=True)

    @staticmethod
    def _sort_key(deal: DealView, sort_by: str) -> float:
        if sort_by == "biggest_discount":
            return float(deal.discount_percent)
        if sort_by == "highest_profit":
            return float(deal.estimated_resale_profit)
        if sort_by == "highest_roi":
            return float(deal.estimated_roi)
        if sort_by == "most_stock":
            return float(deal.stock_level or 0)
        return deal.updated_at.timestamp()
