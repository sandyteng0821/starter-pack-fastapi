"""
advanced_structure/app/main.py
──────────────────────────────
進階版：把 API 層、業務邏輯、schema 分開放。
結構清楚，方便多人協作和後續維護。
"""

from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(
    title="My Tool API",
    description="Tool sharing service — advanced structure.",
    version="1.0.0",
)

app.include_router(router)
