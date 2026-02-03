from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from .base import Base, TimestampMixin


class Entry(Base, TimestampMixin):
    __tablename__ = 'entry'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)

    # Relationships
    responses = relationship('Response', back_populates='entry', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Entry(id={self.id}, content={self.content[:50]}...)>"
