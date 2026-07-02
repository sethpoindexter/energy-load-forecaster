from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.config import DATABASE_URL
from app.models import Base, LoadRecord
import pandas as pd

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def upsert_load_data(df: pd.DataFrame, session=None):
    session = session or SessionLocal()
    records = df.to_dict(orient="records")
    if not records:
        return
    
    insert_fn = sqlite_insert if engine.dialect.name == "sqlite" else pg_insert
    stmt = insert_fn(LoadRecord).values(records)

    stmt = stmt.on_conflict_do_update(
        index_elements=["timestamp"],
        set_={
            "load_mw": stmt.excluded.load_mw,
            "source": stmt.excluded.source
        }
    )

    with session as session:
        session.execute(stmt)
        session.commit()