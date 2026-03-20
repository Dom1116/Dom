from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.deals import router as deals_router
from app.api.v1.stores import router as stores_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(deals_router, prefix="/api/v1")
app.include_router(stores_router, prefix="/api/v1")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
