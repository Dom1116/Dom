# Retail Arbitrage Deal Finder

A full-stack starter for lawful retail arbitrage research across Home Depot, Costco, Walmart, and Target.

## What this starter includes
- Architecture plan and clean-layered backend design.
- PostgreSQL schema for retailers, stores, products, deals, price history, matches, alerts, and watchlists.
- FastAPI backend starter with typed deal endpoint.
- Retailer adapter interface + Walmart example adapter.
- Configurable resale scoring engine with weighted opportunity score.
- Next.js + TypeScript + Tailwind frontend starter.
- **All Store Deals** dashboard page with retailer tabs, store picker, and sortable deals table.

## Folder Structure

```text
.
├── .env.example
├── docs/
│   ├── architecture.md
│   └── database_schema.sql
├── backend/
│   ├── app/
│   │   ├── adapters/
│   │   │   ├── marketplaces/
│   │   │   └── retailers/
│   │   ├── api/v1/
│   │   ├── core/
│   │   ├── jobs/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   └── types/
│   └── tailwind.config.ts
└── index.html (legacy static file)
```

## Backend Quick Start

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API health:

```bash
curl http://localhost:8000/health
```

Deals endpoint example:

```bash
curl -X POST http://localhost:8000/api/v1/deals/all-store \
  -H 'Content-Type: application/json' \
  -d '{"zip_code":"78701","radius_miles":25,"sort_by":"highest_roi"}'
```

## Frontend Quick Start

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Opportunity Score Weights (configurable)
- 30% net profit
- 20% ROI
- 15% marketplace match confidence
- 10% stock availability
- 10% demand / velocity
- 10% competition risk
- 5% category risk

## Compliance Notes
- Use official/public APIs where available.
- Keep browser automation isolated in adapters.
- Respect robots/rate limits/access controls.
- Never fabricate pricing/profitability outputs.
- Include confidence metadata with every estimate.

## Next implementation milestones
1. Add adapters for Home Depot, Costco, and Target.
2. Add real store locator and ZIP/radius geospatial query.
3. Implement persistence repositories and migrations (Alembic/Prisma).
4. Add auth (Clerk/NextAuth) and user settings.
5. Add background scan jobs and alert fanout.
6. Implement compare-stores and card/table toggle UX.
