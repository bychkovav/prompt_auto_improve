from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from .base import Base, TimestampMixin


class Run(Base, TimestampMixin):
    __tablename__ = 'run'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    initial_prompt_id = Column(UUID(as_uuid=True), ForeignKey('prompt_version.id', ondelete='CASCADE'), nullable=False)
    result_prompt_id = Column(UUID(as_uuid=True), ForeignKey('prompt_version.id', ondelete='CASCADE'), nullable=False)
    eval_prompt_id = Column(UUID(as_uuid=True), ForeignKey('eval_prompt.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    initial_prompt = relationship('PromptVersion', back_populates='runs_as_initial', foreign_keys=[initial_prompt_id])
    result_prompt = relationship('PromptVersion', back_populates='runs_as_result', foreign_keys=[result_prompt_id])
    eval_prompt = relationship('EvalPrompt', back_populates='runs', foreign_keys=[eval_prompt_id])
    responses = relationship('Response', back_populates='run', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Run(id={self.id}, initial_prompt_id={self.initial_prompt_id}, result_prompt_id={self.result_prompt_id})>"
