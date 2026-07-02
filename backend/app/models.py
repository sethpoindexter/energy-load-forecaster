from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class LoadRecord(Base):
    __tablename__ = "load_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    load_mw = Column(Float, nullable=False)
    source = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("timestamp", name="uq_timestamp"),
    )