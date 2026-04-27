from pydantic import BaseModel


class ScoreRequest(BaseModel):
    text: str

    model_config = {
        "json_schema_extra": {
            "examples": [{"text": "This compound is highly toxic at low concentrations."}]
        }
    }


class BatchRequest(BaseModel):
    texts: list[str]


class ScoreResponse(BaseModel):
    text: str
    score: float
    label: str


class BatchResponse(BaseModel):
    results: list[ScoreResponse]
