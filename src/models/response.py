from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from .base import Base, TimestampMixin


class Response(Base, TimestampMixin):
    __tablename__ = 'response'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(UUID(as_uuid=True), ForeignKey('run.id', ondelete='CASCADE'), nullable=False)
    entry_id = Column(UUID(as_uuid=True), ForeignKey('entry.id', ondelete='CASCADE'), nullable=False)
    content = Column(Text, nullable=False)

    # Relationships
    run = relationship('Run', back_populates='responses')
    entry = relationship('Entry', back_populates='responses')
    evaluations = relationship('Evaluation', back_populates='response', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Response(id={self.id}, run_id={self.run_id}, entry_id={self.entry_id})>"
