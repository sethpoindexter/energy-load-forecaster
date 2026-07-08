# backend/tests/test_database.py
import pandas as pd
from app.database import upsert_load_data
from app.models import LoadRecord
from datetime import datetime

def test_insert_new_rows(test_session):
    df = pd.DataFrame([
        {"timestamp": datetime(2026, 6, 30, 14), "region": "Central", "load_mw": 100.0, "source": "miso"}
    ])
    upsert_load_data(df, session=test_session)

    rows = test_session.query(LoadRecord).all()
    assert len(rows) == 1
    assert rows[0].load_mw == 100.0


def test_upsert_updates_existing_row(test_session):
    df1 = pd.DataFrame([
        {"timestamp": datetime(2026, 6, 30, 14), "region": "Central", "load_mw": 100.0, "source": "miso"}
    ])
    upsert_load_data(df1, session=test_session)

    df2 = pd.DataFrame([
        {"timestamp": datetime(2026, 6, 30, 14), "region": "Central", "load_mw": 105.5, "source": "miso"}
    ])
    upsert_load_data(df2, session=test_session)

    rows = test_session.query(LoadRecord).all()
    assert len(rows) == 1          # no duplicate
    assert rows[0].load_mw == 105.5  # updated value


def test_same_timestamp_different_regions_coexist(test_session):
    df = pd.DataFrame([
        {"timestamp": datetime(2026, 6, 30, 14), "region": "Central", "load_mw": 100.0, "source": "miso"},
        {"timestamp": datetime(2026, 6, 30, 14), "region": "Midwest", "load_mw": 200.0, "source": "miso"},
        {"timestamp": datetime(2026, 6, 30, 14), "region": "South",   "load_mw": 300.0, "source": "miso"},
    ])
    upsert_load_data(df, session=test_session)

    rows = test_session.query(LoadRecord).all()
    assert len(rows) == 3                              # one row per region
    assert sum(row.load_mw for row in rows) == 600     # total derived on read