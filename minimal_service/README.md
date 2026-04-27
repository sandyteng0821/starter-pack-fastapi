# minimal_service

用最少的 code 把你的工具包成 FastAPI service。  
**唯一需要改的地方：`app.py` 裡的 `calculate_score()` 換成你自己的邏輯。**

## 啟動

```bash
cp .env.example .env        # 設定 port（預設 8001）
pip install -r requirements.txt
python3 app.py
```

打開瀏覽器：`http://127.0.0.1:8001/docs`

## 換成你自己的邏輯

只需要改 `app.py` 中這個 function：

```python
def calculate_score(text: str) -> float:
    # ↓ 換成你的 model / pipeline
    ...
    return score   # 回傳 float
```

如果 input/output 不是文字和分數，同時修改：
- `ScoreRequest` — 定義輸入欄位
- `ScoreResponse` — 定義輸出格式

## Port 衝突？

編輯 `.env`：

```
API_PORT=8002   # 換一個沒人用的 port
```

## Endpoints

| Method | Path          | 說明       |
|--------|---------------|------------|
| GET    | `/`           | Health check |
| POST   | `/score`      | 單筆評分   |
| POST   | `/batch_score`| 批次評分   |
