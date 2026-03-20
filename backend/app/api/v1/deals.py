from fastapi import APIRouter

from app.schemas.deals import DealQuery, DealView
from app.services.deals import DealService

router = APIRouter(prefix="/deals", tags=["deals"])
service = DealService()


@router.post("/all-store", response_model=list[DealView])
async def all_store_deals(payload: DealQuery) -> list[DealView]:
    return await service.get_all_store_deals(payload)
