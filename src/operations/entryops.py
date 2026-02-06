from sqlalchemy import select

from src.models.entry import Entry

def get_next_entry(session, skip: int) -> Optional[dict]:
    q = (
        select(Entry)
        .order_by(Entry.id.asc())
        .offset(skip)
        .limit(1)
    )
    entry = session.execute(q).scalars().first()
    if not entry:
        return None
    return {"entry_id": str(entry.id), "entry_content": entry.content}