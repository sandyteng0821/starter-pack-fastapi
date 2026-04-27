"""
run.py — 啟動入口
啟動：python run.py
"""
import os
import uvicorn


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    port = int(os.getenv("API_PORT", 8001))
    host = os.getenv("API_HOST", "127.0.0.1")
    print(f"Starting on http://{host}:{port}  |  Docs: http://{host}:{port}/docs")
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
