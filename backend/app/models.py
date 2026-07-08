from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class LoadRecord(Base):
    __tablename__ = "load_actuals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    region = Column(String, nullable=False, index=True)
    load_mw = Column(Integer, nullable=False)
    source = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("timestamp", "region", name="uq_timestamp_region"),
    )