from ...services.postgresql_service import Base
from sqlalchemy.sql import func
from sqlalchemy import (
    Column, Integer, String, DateTime, JSON
)

class Cache(Base):
    __tablename__ = "cache"
    key = Column(String(50), primary_key=True, index=True, nullable=False, unique=True)
    value = Column(JSON, nullable=False)
    updated_at = Column(DateTime, nullable=False, server_default=func.now())