# advanced_structure

把 API 層、業務邏輯、schema 分開，方便多人維護和部署。

## 結構

```
advanced_structure/
├── app/
│   ├── main.py              # FastAPI app 和 router 註冊
│   ├── api/
│   │   └── endpoints.py     # 所有 route 定義（只管 HTTP 進出）
│   ├── core/
│   │   └── scorer.py        # 業務邏輯（換成你自己的）
│   └── schemas/
│       └── request.py       # Pydantic input/output schema
├── run.py                   # 啟動入口
├── requirements.txt
├── .env.example
├── Dockerfile
└── docker-compose.yml
```

## 啟動（本地）

```bash
cp .env.example .env
pip install -r requirements.txt
python3 run.py
```

## 啟動（Docker）

```bash
cp .env.example .env
docker compose build
docker compose up -d
```

打開：`http://localhost:8007/docs`

## 換成你自己的邏輯

只需改 `app/core/scorer.py` 裡的 `calculate_score()`。  
`endpoints.py` 和 `main.py` 都不用動。

## 和 minimal_service 的差別

| | minimal_service | advanced_structure |
|--|---|---|
| 檔案數 | 1（app.py） | 分層 |
| 適合 | 快速 demo、個人工具 | 多人協作、準備部署 |
| 改邏輯 | 直接改 app.py | 只改 core/scorer.py |
| Docker | ❌ | ✅ |
