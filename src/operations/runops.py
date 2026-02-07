from models.eval_prompt import EvalPrompt
from models.prompt_version import PromptVersion
from models.run import Run
from sqlalchemy import select, exists, and_
from sqlalchemy.exc import NoResultFound


def create_run(session, initial_prompt_id: str, eval_prompt_id: str) -> dict:
    q = (
        select(PromptVersion)
        .where(PromptVersion.id == initial_prompt_id)
        .limit(1)
    ) 
    initial_prompt = session.execute(q).scalars().first()

    if initial_prompt is None:
        raise NoResultFound(f"PromptVersion with id={initial_prompt_id} not found")
    
    qe = (
        select(EvalPrompt)
        .where(EvalPrompt.id == eval_prompt_id)
        .limit(1)
    ) 

    eval_prompt = session.execute(qe).scalars().first()

    if eval_prompt is None:
        raise NoResultFound(f"EvalPrompt with id={eval_prompt_id} not found")

    # 2) create run; result_prompt_id starts as initial
    run = Run(
        initial_prompt_id=initial_prompt_id,
        eval_prompt_id=eval_prompt_id,
    )
    session.add(run)
    session.commit()

    return {
        "run_id": str(run.id),
        "initial_prompt_id": str(run.initial_prompt_id),
        "initial_prompt_content": initial_prompt.content,
        "eval_prompt_content": eval_prompt.content,
        "processed_count": 0
    }