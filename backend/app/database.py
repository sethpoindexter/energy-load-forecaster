from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.config import DATABASE_URL
from app.models import Base, LoadRecord
import pandas as pd

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Chunk rows so a single INSERT never exceeds max bound variables
MAX_BIND_PARAMS = 900

def init_db():
    Base.metadata.create_all(bind=engine)

def upsert_load_data(df: pd.DataFrame, session=None):
    session = session or SessionLocal()
    records = df.to_dict(orient="records")
    if not records:
        return

    insert_fn = sqlite_insert if engine.dialect.name == "sqlite" else pg_insert
    chunk_size = max(1, MAX_BIND_PARAMS // len(df.columns))

    with session as session:
        for start in range(0, len(records), chunk_size):
            chunk = records[start:start + chunk_size]
            stmt = insert_fn(LoadRecord).values(chunk)
            stmt = stmt.on_conflict_do_update(
                index_elements=["timestamp", "region"],
                set_={
                    "load_mw": stmt.excluded.load_mw,
                    "source": stmt.excluded.source
                }
            )
            session.execute(stmt)
        session.commit()