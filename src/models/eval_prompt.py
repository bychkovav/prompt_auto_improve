from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from .base import Base, TimestampMixin


class EvalPrompt(Base, TimestampMixin):
    __tablename__ = 'eval_prompt'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)

    # Relationships
    runs = relationship('Run', back_populates='eval_prompt', foreign_keys='Run.eval_prompt_id')

    def __repr__(self):
        return f"<EvalPrompt(id={self.id}, content={self.content[:50]}...)>"
