# Retail Arbitrage Deal Finder

Production-style starter you can run **today** with Docker or local dev.

## What works right now
- API serving store-level deals for Home Depot, Costco, Walmart, and Target from a demo dataset.
- All Store Deals page is wired to backend API (not static frontend mock state).
- ZIP/radius store lookup endpoint and store selector.
- Sorting, clearance toggle, high resale toggle, search filter.
- Opportunity scoring engine with configurable weights.

## 1-minute start (Docker)
```bash
docker compose up --build
```
Then open:
- Frontend: http://localhost:3000
- Backend health: http://localhost:8000/health
- Deals API: `POST http://localhost:8000/api/v1/deals/all-store`

## Local dev (without Docker)
### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Core API endpoints
- `GET /api/v1/stores/nearby?zip_code=78701&radius_miles=25`
- `POST /api/v1/deals/all-store`

Sample request:
```json
{
  "retailer_codes": ["walmart", "target"],
  "zip_code": "78701",
  "radius_miles": 25,
  "store_ids": [],
  "min_profit": 10,
  "min_roi": 20,
  "clearance_only": false,
  "high_resale_only": false,
  "sort_by": "highest_roi",
  "page": 1,
  "page_size": 25
}
```

## Architecture + schema
- Architecture plan: `docs/architecture.md`
- SQL schema: `docs/database_schema.sql`

## Next upgrades
1. Replace demo catalog with persisted scan ingestion.
2. Add real adapters + job queues (Celery/Redis) + retries/rate limiting.
3. Add auth, favorites, watchlists, alert delivery channels.
