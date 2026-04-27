from typing import List
"""
minimal_service/app.py
──────────────────────
最小可行的 FastAPI service。
把你自己的邏輯換進 `calculate_score()`，其他都不用動。

啟動：python app.py
文件：http://127.0.0.1:8001/docs
"""

from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(
    title="My Tool API",
    description="把你的工具包成 API。換掉 calculate_score() 就好。",
    version="0.1.0",
)


# ── 1. 定義 input / output schema ─────────────────────────────────────────────

class ScoreRequest(BaseModel):
    text: str

    model_config = {
        "json_schema_extra": {
            "examples": [{"text": "This compound is highly toxic at low concentrations."}]
        }
    }


class ScoreResponse(BaseModel):
    text: str
    score: float        # 0.0（低風險）→ 1.0（高風險）
    label: str          # "low" / "medium" / "high"


class BatchRequest(BaseModel):
    texts: List[str]


class BatchResponse(BaseModel):
    results: List[ScoreResponse]


# ── 2. 你的業務邏輯（換成自己的 function）────────────────────────────────────

# 示範用的 keyword-based scorer。
# 換成你自己的 model / pipeline 就好，介面（輸入 str → 輸出 float）不變。
_HIGH_RISK = ["toxic", "harmful", "poison", "lethal", "carcinogen", "hazardous"]
_MED_RISK  = ["irritant", "caution", "warning", "concentration", "exposure"]

def calculate_score(text: str) -> float:
    """
    輸入文字，回傳 0.0 ~ 1.0 的風險分數。
    ↑ 換成你自己的邏輯 ↑
    """
    text_lower = text.lower()
    score = 0.0
    for kw in _HIGH_RISK:
        if kw in text_lower:
            score += 0.3
    for kw in _MED_RISK:
        if kw in text_lower:
            score += 0.1
    return min(score, 1.0)


def score_to_label(score: float) -> str:
    if score >= 0.6:
        return "high"
    elif score >= 0.3:
        return "medium"
    return "low"


# ── 3. 包成 endpoint ──────────────────────────────────────────────────────────

@app.get("/", summary="Health check")
def root():
    return {"status": "running", "service": "My Tool API"}


@app.post("/score", response_model=ScoreResponse, summary="單筆評分")
def score(req: ScoreRequest):
    """
    輸入一段文字，回傳風險分數（0~1）和等級（low / medium / high）。
    """
    s = calculate_score(req.text)
    return ScoreResponse(text=req.text, score=round(s, 3), label=score_to_label(s))


@app.post("/batch_score", response_model=BatchResponse, summary="批次評分")
def batch_score(req: BatchRequest):
    """
    一次送多筆文字，逐筆回傳結果。
    """
    results = []
    for text in req.texts:
        s = calculate_score(text)
        results.append(ScoreResponse(text=text, score=round(s, 3), label=score_to_label(s)))
    return BatchResponse(results=results)


# ── 4. 啟動 ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8001))
    host = os.getenv("API_HOST", "127.0.0.1")
    print(f"Starting on http://{host}:{port}  |  Docs: http://{host}:{port}/docs")
    uvicorn.run("app:app", host=host, port=port, reload=True)
