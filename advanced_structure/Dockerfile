FROM python:3.11-slim

WORKDIR /app

# 先裝套件（利用 Docker cache：套件沒變就不用重裝）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再複製 code
COPY . .

EXPOSE ${API_PORT:-8007}

CMD ["sh", "-c", "uvicorn app.main:app --host ${API_HOST:-0.0.0.0} --port ${API_PORT:-8007}"]
