from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func


class SystemSetting(Base):
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)   # e.g., commission_rate
    value = Column(Text, nullable=False)                     # e.g., 5.0
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
