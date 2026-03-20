from fastapi import APIRouter, Query

from app.schemas.deals import StoreView
from app.services.deals import DealService

router = APIRouter(prefix="/stores", tags=["stores"])
service = DealService()


@router.get("/nearby", response_model=list[StoreView])
async def nearby_stores(
    zip_code: str = Query(default="78701"),
    radius_miles: int = Query(default=25, ge=1, le=100),
    retailer_codes: list[str] = Query(default=[]),
) -> list[StoreView]:
    return service.nearby_stores(zip_code=zip_code, radius_miles=radius_miles, retailer_codes=retailer_codes)
