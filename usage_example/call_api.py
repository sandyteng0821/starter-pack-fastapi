"""
usage_example/call_api.py
─────────────────────────
呼叫別人（或自己）的 FastAPI 服務範例。
只需要改 BASE_URL，其他邏輯不用動。

前置：pip install requests
"""

import requests

# ── 改這裡：換成你要 call 的 server ──────────────────────────────────────────
BASE_URL = "http://127.0.0.1:8001"
# ─────────────────────────────────────────────────────────────────────────────


def health_check():
    """確認 server 還活著。"""
    res = requests.get(f"{BASE_URL}/")
    res.raise_for_status()
    print("[health]", res.json())


def call_score(text: str):
    """呼叫 /score endpoint，傳入文字，取得分數。"""
    payload = {"text": text}
    res = requests.post(f"{BASE_URL}/score", json=payload)
    res.raise_for_status()
    return res.json()


def call_batch(texts: list):
    """一次送多筆文字。"""
    payload = {"texts": texts}
    res = requests.post(f"{BASE_URL}/batch_score", json=payload)
    res.raise_for_status()
    return res.json()


if __name__ == "__main__":
    # 1. health check
    health_check()

    # 2. 單筆
    result = call_score("This product contains harmful chemicals at high concentration.")
    print("[single]", result)

    # 3. 批次
    results = call_batch([
        "water at trace levels",
        "extremely toxic compound, do not inhale",
        "mild irritant, use with care",
    ])
    print("[batch]")
    for r in results["results"]:
        print(f"  {r['score']:.2f}  {r['label']:<8}  {r['text'][:50]}")
