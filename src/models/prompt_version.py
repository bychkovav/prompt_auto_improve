from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from .base import Base, TimestampMixin


class PromptVersion(Base, TimestampMixin):
    __tablename__ = 'prompt_version'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    meta = Column(JSONB, nullable=True)

    # Relationships
    runs_as_initial = relationship('Run', back_populates='initial_prompt', foreign_keys='Run.initial_prompt_id')
    runs_as_result = relationship('Run', back_populates='result_prompt', foreign_keys='Run.result_prompt_id')

    def __repr__(self):
        return f"<PromptVersion(id={self.id}, content={self.content[:50]}...)>"
