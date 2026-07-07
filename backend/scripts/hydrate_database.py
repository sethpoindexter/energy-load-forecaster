from ingestion import MISODataSource
from app.database import SessionLocal, upsert_load_data, init_db
from ingestion import normalize
from datetime import datetime
import pandas as pd

START_DATE = datetime(2026, 6, 1, 0)     # June 1,  2026, 0:00  UTC
END_DATE   = datetime(2026, 6, 14, 23)   # June 14, 2026, 23:00 UTC

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