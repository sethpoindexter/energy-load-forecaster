from ingestion import MISODataSource
from app.database import SessionLocal, upsert_load_data, init_db
from ingestion import normalize
from datetime import datetime
import pandas as pd

# Dates are in EST timezone
START_DATE = datetime(2025, 6, 1, 0)
END_DATE   = datetime(2026, 6, 30, 23)

def hydrate():
    data_source = MISODataSource()
    raw_data: list[dict] = data_source.fetch(start=START_DATE, end=END_DATE)

    if not raw_data:
        return

    clean_data: pd.DataFrame = normalize(raw_data, "miso")

    init_db()

    with SessionLocal() as session:
        upsert_load_data(df=clean_data, session=session)

hydrate()