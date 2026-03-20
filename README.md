# Retail Arbitrage Deal Finder (Personal Use)

This project is a **personal-use deal finder** to help you scan local deals from Home Depot, Costco, Walmart, and Target and quickly rank items for resale potential.

No SaaS billing, no pricing plans, no multi-tenant complexity — just a practical stack you can run and extend.

## What’s implemented now
- FastAPI backend with a real `/api/v1/deals/all-store` endpoint.
- Modular retailer adapter interface and a personal sample adapter set for all 4 retailers.
- Next.js frontend that opens directly to **All Store Deals**.
- ZIP/radius/store selector with local favorite-store saving.
- Filtering by retailer + sorting by discount/profit/ROI/newest/stock.
- Configurable opportunity scoring engine.

## Architecture + schema
- Architecture plan: `docs/architecture.md`
- SQL schema: `docs/database_schema.sql`

## Run backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Run frontend
```bash
cd frontend
npm install
npm run dev
```

Then open `http://localhost:3000`.

## Environment config
Copy values from `.env.example`.

## Notes
- Current adapters are personal starter data so you can iterate quickly.
- Replace sample adapters with official APIs (or compliant browser automation) when you are ready.
- Keep usage lawful and respect rate limits/access rules.
