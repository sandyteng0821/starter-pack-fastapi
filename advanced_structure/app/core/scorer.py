"""
app/core/scorer.py
──────────────────
業務邏輯層，和 API 層完全分開。
換掉這裡的 calculate_score()，API 層不用動。
"""

_HIGH_RISK = ["toxic", "harmful", "poison", "lethal", "carcinogen", "hazardous"]
_MED_RISK  = ["irritant", "caution", "warning", "concentration", "exposure"]


def calculate_score(text: str) -> float:
    """
    輸入文字，回傳 0.0 ~ 1.0 風險分數。
    換成你自己的 model 或 pipeline。
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
