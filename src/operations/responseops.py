from sqlalchemy import select
from src.models.entry import Entry
from src.models.evaluation import Evaluation
from src.models.prompt_version import PromptVersion
from src.models.response import Response
from sqlalchemy.exc import NoResultFound

from src.models.run import Run

def create_response(session, run_id: str, entry_id: str, content: str) -> str:
    r = Response(run_id=run_id, entry_id=entry_id)
    session.add(r)
    session.commit()
    
    return str(r.id)

def set_content(session, response_id: str, content: str) -> None:
    r = session.get(Response, response_id)
    if not r:
        raise NoResultFound(f"Response with id={response_id} not found")

    r.content = content
    session.commit()

def sample_recent_examples(session, eval_prompt_id: str, k_runs: int = 3, n_samples: int = 3):
    runs = session.execute(
        select(Run)
        .where(Run.eval_prompt_id == eval_prompt_id)
        .order_by(Run.created_date.desc())
        .limit(k_runs)
    ).scalars().all()

    if not runs:
        return []

    candidates = []
    for run in runs:
        rows = session.execute(
            select(PromptVersion, Response, Entry, Evaluation)
            .join(Response, Response.run_id == Run.id)
            .join(Entry, Entry.id == Response.entry_id)
            .join(Evaluation, Evaluation.response_id == Response.id)
            .join(PromptVersion, PromptVersion.id == run.result_prompt_id)
            .where(Run.id == run.id)
            .limit(n_samples)
        ).all()

        for pv, resp, entry, ev in rows:
            candidates.append({
                "prompt_version_id": str(pv.id),
                "prompt_content": pv.content,
                "output": resp.content,         
                "input": entry.content,
                "score": ev.score,
            })

    if not candidates:
        return []

    return candidates