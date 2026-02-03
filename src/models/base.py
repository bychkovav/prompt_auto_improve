from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class TimestampMixin:
    """Mixin to add created_date and updated_date to models"""
    created_date = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_date = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
