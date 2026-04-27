# FastAPI Starter Pack

把你的工具包成 API，讓整個團隊都可以用。

## 從哪裡開始

```
我只想 call 別人的 API
→  usage_example/

我想把自己的工具包成 API（單檔，快速）
→  minimal_service/

我想要乾淨的結構 + Docker，準備部署
→  advanced_structure/
```

## 結構

```
starter_pack/
├── usage_example/          ← call 現有 API（零門檻）
│   ├── call_api.py
│   └── README.md
│
├── minimal_service/        ← 把工具包成 API（單檔）
│   ├── app.py              ← 主要改這裡
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
└── advanced_structure/     ← 分層結構 + Docker
    ├── app/
    │   ├── main.py
    │   ├── api/endpoints.py
    │   ├── core/scorer.py  ← 主要改這裡
    │   └── schemas/request.py
    ├── run.py
    ├── .env.example
    ├── Dockerfile
    ├── docker-compose.yml
    └── README.md
```

## Demo 邏輯說明

三個資料夾都用同一個 demo 邏輯：**keyword-based 文字風險評分器**。  
輸入一段文字，回傳 0~1 的風險分數和等級（low / medium / high）。

這只是 demo，**換成你自己的 function 就好**，API 介面不用動。

## Port 管理

每個人本地開發用不同 port，放在 `.env` 裡：

```
API_PORT=8001   # 同事 A
API_PORT=8002   # 同事 B
API_PORT=8003   # 同事 C
```

## 分享投影片

→ [FAST_API_GUIDE.pdf](./FAST_API_GUIDE.pdf)