# usage_example

呼叫別人的 API，不需要看對方 source code，也不需要 setup 對方的環境。

## 步驟

```bash
pip install requests
# 先確認對方的 service 已經跑起來

python call_api.py
```

## 如果要改 endpoint

打開 `call_api.py`，只需改一行：

```python
BASE_URL = "http://127.0.0.1:8001"   # ← 換成目標 server
```

## Swagger UI（不寫 code 也可以測試）

每個 FastAPI service 都有自動產生的互動文件：

```
http://127.0.0.1:8001/docs
```

用瀏覽器打開，填參數，按 Execute。
