from src.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


class AbstractBase(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
