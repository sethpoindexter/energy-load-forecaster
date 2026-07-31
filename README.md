# Energy Load Forecasting Model + Dashboard

Short-term electricity load forecasting using Midcontinent Independent System
Operator data. The system will ingest load data on a schedule, forecast system demand for the
next 1–6 hours with a custom ML model, and serve actuals + the rolling forecast to an
interactive web dashboard.

**Stack:** Python · FastAPI · SQLAlchemy 2.0 (SQLite in dev → Postgres in prod) · scikit-learn ·
Vite + React + Recharts.

## Current State

Currently in the modeling phase. A forecast model is prototyped and evaluated at backend/notebooks/02_modeling.ipynb.

**Highlights**
- **EDA-driven features.** ACF/PACF showed load is dominated by the last 1–2 hours and a strong daily cycle, so the model uses recent lags (1h/2h/24h) + cyclical hour/day-of-year + a weekend flag.
- **Noted missing signals.** Same-hour load spread peaks in the afternoon, likely due to cooling demand, so noting temperature as the next feature and where forecast error may occur.
- **Results.** Separate per-horizon models with a chronological split. The gradient-boosted model beats a seasonal-naive baseline by ~86% / 56% / 29% skill at 1h / 3h / 6h (1h MAPE 0.63%).

**Done**
- Database schema (`load_actuals`)
- MISO data ingestion via API (~2.8 years of history pulled)
- Major exploratory data analysis + feature selection
- Baselines + gradient-boosted model, evaluated per horizon (1h/3h/6h)

**In progress**
- Extracting the feature + model pipeline into shared modules
- Scheduled ingestion to keep data current for live forecasting

## Next Steps

1. **Serve forecasts** — FastAPI endpoints for actuals, forecast, and metrics
2. **Dashboard** — React chart with the forecast and actual load data
3. **Deploy**

## AI Usage
Backend and modeling completed with some AI assistance.
Frontend, when implemented, will feature heavy AI assistance.
