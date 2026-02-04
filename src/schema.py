from typing import TypedDict, Optional, List, Dict, Any
from uuid import UUID

class RecentExample(TypedDict):
    prompt_version_id: str
    prompt_content: str
    output: str
    score: Dict[str, Any]  # your JSONB score payload

class State(TypedDict, total=False):
    # Inputs
    initial_prompt_content: str
    eval_prompt_id: str
    eval_prompt_content: str
    max_items: int

    # Run context
    run_id: str
    result_prompt_id: str     # current prompt_version.id used for generation
    result_prompt_content: str

    # Current loop item context
    entry_id: Optional[str]
    entry_content: Optional[str]
    response_id: Optional[str]
    model_output: Optional[str]
    evaluation_score: Optional[Dict[str, Any]]

    # Prompt improvement context
    recent_examples: List[RecentExample]
    proposed_prompt_content: Optional[str]
    proposed_prompt_version_id: Optional[str]

    processed_count: int