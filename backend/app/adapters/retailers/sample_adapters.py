from datetime import datetime

from app.adapters.retailers.base import NormalizedRetailDeal, RetailerAdapter


class StaticRetailerAdapter(RetailerAdapter):
    """Personal-use adapter backed by static/sample data.

    Replace `seed_rows` with API or compliant browser collection in production.
    """

    def __init__(self, code: str, seed_rows: list[dict]) -> None:
        self.code = code
        self.seed_rows = seed_rows

    async def fetch_store_deals(self, *, zip_code: str, radius_miles: int, store_ids: list[str] | None = None) -> list[NormalizedRetailDeal]:
        allowed = set(store_ids or [])
        rows: list[NormalizedRetailDeal] = []
        for row in self.seed_rows:
            if allowed and row["store_id"] not in allowed:
                continue
            rows.append(
                NormalizedRetailDeal(
                    retailer_code=self.code,
                    store_id=row["store_id"],
                    store_number=row.get("store_number"),
                    item_id=row["item_id"],
                    title=row["title"],
                    brand=row.get("brand"),
                    upc=row.get("upc"),
                    current_price=row["current_price"],
                    original_price=row.get("original_price"),
                    stock_level=row.get("stock_level"),
                    inventory_status=row.get("inventory_status", "unknown"),
                    markdown_label=row.get("markdown_label"),
                    product_url=row.get("product_url"),
                    image_url=row.get("image_url"),
                    category=row.get("category"),
                    fetched_at=datetime.utcnow(),
                )
            )
        return rows


def build_personal_adapters() -> dict[str, RetailerAdapter]:
    return {
        "walmart": StaticRetailerAdapter(
            "walmart",
            [
                {
                    "store_id": "wm-1001",
                    "store_number": "1001",
                    "item_id": "WM-123",
                    "title": "Cordless Impact Driver Kit",
                    "brand": "HyperTough",
                    "upc": "012345678901",
                    "current_price": 49.0,
                    "original_price": 89.0,
                    "stock_level": 8,
                    "inventory_status": "in_stock",
                    "markdown_label": "Clearance",
                    "category": "Tools",
                    "product_url": "https://www.walmart.com/ip/demo-impact-driver",
                    "image_url": "https://picsum.photos/300/300",
                }
            ],
        ),
        "target": StaticRetailerAdapter(
            "target",
            [
                {
                    "store_id": "tg-204",
                    "store_number": "T-204",
                    "item_id": "TG-55",
                    "title": "LEGO Creator Set",
                    "brand": "LEGO",
                    "upc": "333222111999",
                    "current_price": 19.99,
                    "original_price": 39.99,
                    "stock_level": 3,
                    "inventory_status": "low_stock",
                    "markdown_label": "Sale",
                    "category": "Toys",
                    "product_url": "https://www.target.com/p/demo-lego",
                    "image_url": "https://picsum.photos/301/300",
                }
            ],
        ),
        "homedepot": StaticRetailerAdapter(
            "homedepot",
            [
                {
                    "store_id": "hd-402",
                    "store_number": "402",
                    "item_id": "HD-901",
                    "title": "Ryobi 18V Battery 2-Pack",
                    "brand": "Ryobi",
                    "current_price": 59.0,
                    "original_price": 99.0,
                    "stock_level": 6,
                    "inventory_status": "in_stock",
                    "markdown_label": "Strong store-specific clearance",
                    "category": "Tools",
                    "product_url": "https://www.homedepot.com/p/demo-ryobi",
                    "image_url": "https://picsum.photos/302/300",
                }
            ],
        ),
        "costco": StaticRetailerAdapter(
            "costco",
            [
                {
                    "store_id": "co-18",
                    "store_number": "18",
                    "item_id": "CO-440",
                    "title": "Ninja Blender Bundle",
                    "brand": "Ninja",
                    "current_price": 79.99,
                    "original_price": 129.99,
                    "stock_level": 14,
                    "inventory_status": "in_stock",
                    "markdown_label": "Confirmed current price",
                    "category": "Kitchen",
                    "product_url": "https://www.costco.com/demo-ninja",
                    "image_url": "https://picsum.photos/303/300",
                }
            ],
        ),
    }
