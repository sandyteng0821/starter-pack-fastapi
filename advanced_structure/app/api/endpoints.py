from fastapi import APIRouter
from app.schemas.request import (
    ScoreRequest, ScoreResponse,
    BatchRequest, BatchResponse,
)
from app.core.scorer import calculate_score, score_to_label

router = APIRouter()


@router.get("/", summary="Health check")
def root():
    return {"status": "running"}


@router.post("/score", response_model=ScoreResponse, summary="單筆評分")
def score(req: ScoreRequest):
    s = calculate_score(req.text)
    return ScoreResponse(text=req.text, score=round(s, 3), label=score_to_label(s))


@router.post("/batch_score", response_model=BatchResponse, summary="批次評分")
def batch_score(req: BatchRequest):
    results = []
    for text in req.texts:
        s = calculate_score(text)
        results.append(
            ScoreResponse(text=text, score=round(s, 3), label=score_to_label(s))
        )
    return BatchResponse(results=results)
