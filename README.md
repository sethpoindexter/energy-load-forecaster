# Energy Load Forecasting Dashboard

Short-term electricity load forecasting using Midcontinent Independent System
Operator data. The system ingests load data on a schedule, forecasts system demand for the
next 1–6 hours with a custom ML model, and serves live actuals + the rolling forecast to an
interactive web dashboard.

**Stack:** Python · FastAPI · SQLAlchemy 2.0 (SQLite in dev → Postgres in prod) · scikit-learn ·
Vite + React + Recharts.

## Current State

Currently in exploratory data analysis phase to choose features for the model.

**Done**
- Database schema
- MISO data ingestion up to the day via API
- Major exploratory data analysis

**In progress**
- Model analysis
- FastAPI backend
- Read-only API endpoints for actual load data and forecasted load data

## Next Steps

1. **Baselines** — persistence and seasonal-naive forecasts to set a baseline
3. **ML model** — feature pipeline (lags, cyclical calendar features...)
4. **Serve forecasts** — grab actuals and forecasts with backend API endpoints
5. **Dashboard** — React chart with the forecast and actual load data
6. **Deploy**

## AI Usage
Backend and modeling written by hand with very minor AI assistance.
Frontend, when implemented, will feature heavy AI assistance.
