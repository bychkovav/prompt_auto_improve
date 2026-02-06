from src.models.evaluation import Evaluation


def create_evaluation(session, response_id: str, score: dict) -> str:
    e = Evaluation(response_id=response_id, score=score)
    session.add(e)
    session.commit()
    return str(e.id)