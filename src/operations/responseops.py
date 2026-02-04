from src.models.response import Response

def db_create_response(session, run_id: str, entry_id: str, content: str) -> str:
    r = Response(run_id=run_id, entry_id=entry_id)
    session.add(r)
    session.commit()
    
    return str(r.id)