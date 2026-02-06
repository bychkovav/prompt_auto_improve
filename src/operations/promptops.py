from datetime import datetime, timezone
from src.models.prompt_version import PromptVersion
from src.models.run import Run
from sqlalchemy.exc import NoResultFound


def create_prompt_version_for_run(session, run_id: str, new_prompt_content: str) -> dict:
    run = session.get(Run, run_id)
    if not run:
        raise NoResultFound(f"Run with id={run_id} not found")
    
    pv = PromptVersion(content=new_prompt_content)
    session.add(pv)
    session.flush()

    run.result_prompt_id = pv.id
    session.commit()

    return {"result_prompt_id": str(pv.id), "result_prompt_content": pv.content}
