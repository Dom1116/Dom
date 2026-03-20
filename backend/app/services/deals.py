from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal

from app.schemas.deals import DealQuery, DealView, StoreView


@dataclass
class DemoStore:
    id: int
    retailer_code: str
    retailer_name: str
    store_number: str
    name: str
    city: str
    state: str
    zip_code: str
    distance_miles: float


@dataclass
class DemoDeal:
    retailer_code: str
    retailer_name: str
    store_id: int
    store_location: str
    store_number: str
    product_title: str
    brand: str
    sku_item_id: str
    upc_gtin: str
    current_price: float
    original_price: float
    clearance_label: str
    stock_level: int
    deal_confidence: float
    product_url: str
    image_url: str
    estimated_resale_profit: float
    estimated_roi: float
    updated_at: datetime


class DealService:
    """Production-ready shape with demo catalog, enabling immediate local use today."""

    def __init__(self) -> None:
        now = datetime.utcnow()
        self.stores = [
            DemoStore(101, "walmart", "Walmart", "1001", "Walmart Supercenter", "Austin", "TX", "78701", 2.1),
            DemoStore(201, "target", "Target", "T204", "Target North", "Austin", "TX", "78758", 4.7),
            DemoStore(301, "homedepot", "Home Depot", "402", "Home Depot Lamar", "Austin", "TX", "78757", 5.2),
            DemoStore(401, "costco", "Costco", "18", "Costco Research Blvd", "Austin", "TX", "78759", 7.1),
        ]
        self.deals = [
            DemoDeal("walmart", "Walmart", 101, "Austin, TX", "1001", "Cordless Impact Driver Kit", "HyperTough", "WM-123", "012345678901", 49, 89, "clearance", 8, 0.83, "https://www.walmart.com/ip/demo", "https://picsum.photos/200?1", 20.35, 41.53, now - timedelta(hours=2)),
            DemoDeal("target", "Target", 201, "Austin, TX", "T204", "LEGO Creator 3-in-1", "LEGO", "TG-55", "333222111999", 19.99, 39.99, "sale", 3, 0.74, "https://www.target.com/p/demo", "https://picsum.photos/200?2", 14.1, 70.49, now - timedelta(hours=5)),
            DemoDeal("homedepot", "Home Depot", 301, "Austin, TX", "402", "Milwaukee Hammer Drill", "Milwaukee", "HD-88", "888111444222", 79, 149, "clearance", 6, 0.89, "https://www.homedepot.com/p/demo", "https://picsum.photos/200?3", 42.2, 53.42, now - timedelta(hours=1)),
            DemoDeal("costco", "Costco", 401, "Austin, TX", "18", "Ninja Blender Pro", "Ninja", "CO-77", "555777888111", 59.99, 99.99, "warehouse markdown", 12, 0.78, "https://www.costco.com/demo", "https://picsum.photos/200?4", 24.88, 41.47, now - timedelta(minutes=25)),
        ]

    def nearby_stores(self, zip_code: str, radius_miles: int, retailer_codes: list[str] | None = None) -> list[StoreView]:
        rows = [s for s in self.stores if s.distance_miles <= radius_miles]
        if retailer_codes:
            wanted = {code.lower() for code in retailer_codes}
            rows = [s for s in rows if s.retailer_code in wanted]
        return [
            StoreView(
                id=s.id,
                retailer_code=s.retailer_code,
                retailer_name=s.retailer_name,
                store_number=s.store_number,
                name=s.name,
                city=s.city,
                state=s.state,
                zip_code=s.zip_code,
                distance_miles=s.distance_miles,
            )
            for s in sorted(rows, key=lambda v: v.distance_miles)
        ]

    async def get_all_store_deals(self, query: DealQuery) -> list[DealView]:
        rows = list(self.deals)

        if query.retailer_codes:
            wanted = {code.lower() for code in query.retailer_codes}
            rows = [d for d in rows if d.retailer_code in wanted]

        if query.store_ids:
            selected = set(query.store_ids)
            rows = [d for d in rows if d.store_id in selected]

        if query.compare_store_ids:
            selected = set(query.compare_store_ids)
            rows = [d for d in rows if d.store_id in selected]

        if query.min_profit is not None:
            rows = [d for d in rows if d.estimated_resale_profit >= query.min_profit]

        if query.min_roi is not None:
            rows = [d for d in rows if d.estimated_roi >= query.min_roi]

        if query.clearance_only:
            rows = [d for d in rows if "clearance" in d.clearance_label]

        if query.high_resale_only:
            rows = [d for d in rows if d.estimated_roi >= 40 and d.estimated_resale_profit >= 20]

        if query.search:
            search = query.search.lower()
            rows = [d for d in rows if search in d.product_title.lower() or search in d.brand.lower()]

        def key_func(deal: DemoDeal) -> float | datetime:
            if query.sort_by == "biggest_discount":
                return (deal.original_price - deal.current_price) / max(deal.original_price, 1)
            if query.sort_by == "highest_profit":
                return deal.estimated_resale_profit
            if query.sort_by == "highest_roi":
                return deal.estimated_roi
            if query.sort_by == "most_stock":
                return deal.stock_level
            return deal.updated_at

        rows = sorted(rows, key=key_func, reverse=True)

        start = (query.page - 1) * query.page_size
        end = start + query.page_size
        page_rows = rows[start:end]

        return [
            DealView(
                retailer_name=d.retailer_name,
                retailer_code=d.retailer_code,
                store_id=d.store_id,
                store_location=d.store_location,
                store_number=d.store_number,
                product_title=d.product_title,
                brand=d.brand,
                sku_item_id=d.sku_item_id,
                upc_gtin=d.upc_gtin,
                current_price=Decimal(str(d.current_price)),
                original_price=Decimal(str(d.original_price)),
                discount_percent=round(((d.original_price - d.current_price) / d.original_price) * 100, 2),
                clearance_label=d.clearance_label,
                stock_level=d.stock_level,
                deal_confidence=d.deal_confidence,
                product_url=d.product_url,
                image_url=d.image_url,
                estimated_resale_profit=Decimal(str(d.estimated_resale_profit)),
                estimated_roi=Decimal(str(d.estimated_roi)),
                updated_at=d.updated_at,
            )
            for d in page_rows
        ]
