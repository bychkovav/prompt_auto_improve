from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from .base import Base, TimestampMixin


class Evaluation(Base, TimestampMixin):
    __tablename__ = 'evaluation'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    response_id = Column(UUID(as_uuid=True), ForeignKey('response.id', ondelete='CASCADE'), nullable=False)
    score = Column(JSONB, nullable=False)

    # Relationships
    response = relationship('Response', back_populates='evaluations')

    def __repr__(self):
        return f"<Evaluation(id={self.id}, response_id={self.response_id}, score={self.score})>"
