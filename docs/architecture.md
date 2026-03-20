# Retail Arbitrage Deal Finder - Architecture Plan

## 1) System Overview
The platform is a modular full-stack application for lawful, store-level deal discovery and resale opportunity analysis across Home Depot, Costco, Walmart, and Target.

### Core goals
- Aggregate store-specific deals from supported retailers.
- Let users select ZIP/radius/store and compare opportunities.
- Score products by profitability, ROI, confidence, and risk.
- Provide alerts and watchlist-driven monitoring.

## 2) High-Level Architecture
- **Frontend (Next.js + TypeScript + Tailwind):** dashboard, filters, store selection, comparison and product detail pages.
- **Backend API (FastAPI + SQLAlchemy):** typed REST endpoints, auth integration, deal search, scoring, alerts.
- **Workers (Celery):** scheduled scans, price history updates, markdown detection, alert fanout.
- **PostgreSQL:** primary relational store.
- **Redis:** cache + broker/rate-limiter state.

## 3) Layers (Clean Architecture)
1. **Adapters Layer:** retailer collectors and marketplace match adapters.
2. **Service Layer:** deal orchestration, ranking, alerting, markdown rules.
3. **Repository Layer:** persistence and query composition.
4. **API Layer:** HTTP DTOs and endpoint handlers.
5. **Jobs Layer:** async scan and notification tasks.

## 4) Ingestion Pipeline
1. Scheduler enqueues `scan_retailer_store` jobs.
2. Adapter pulls normalized product/deal data with retries and rate limits.
3. Service validates + enriches records.
4. Repository upserts stores/products/store_products.
5. Price deltas appended to `price_history`.
6. Marketplace matcher updates `marketplace_matches` and `resale_estimates`.
7. Alert engine evaluates rules and emits notifications.

## 5) Key Domain Modules
- `DealService`: store-centric deal retrieval/filtering/sorting.
- `StoreService`: ZIP/radius lookup, favorites, compare selections.
- `ResaleScoringService`: opportunity score + confidence.
- `MarkdownRulesEngine`: hidden clearance candidates.
- `AlertService`: rule evaluation + dispatch.

## 6) Security & Compliance
- Respect robots/rate limits/public-access rules.
- No CAPTCHA bypass, auth circumvention, or scraping behind protected walls.
- Persist source metadata and confidence for every estimate.

## 7) Observability
- Structured logs with retailer/store context.
- Metrics: scan success rate, adapter latency, stale inventory counts.
- Admin views: parser health, failed scans, anomaly queue, scoring settings.

## 8) Scaling Notes
- Horizontal API workers behind load balancer.
- Queue partitioning by retailer and region.
- Indexes on store/product/price history dimensions.
- Redis-backed short-TTL cache for hot deal queries.
