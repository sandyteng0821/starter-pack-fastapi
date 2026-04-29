# Background Knowledge

Tech sharing 補充說明：網路與 Docker 基礎概念。  
如果 Demo 3 有任何看不懂的地方，這份文件可以幫你補背景。

---

## 目錄

1. [IP 位址：127.0.0.1 vs 0.0.0.0 vs Server IP](#1-ip-位址)
2. [Port 是什麼，怎麼查](#2-port-是什麼怎麼查)
3. [.env 檔案是什麼，為什麼要用](#3-env-檔案)
4. [Container 是什麼](#4-container-是什麼)
5. [Docker 常用指令速查](#5-docker-常用指令速查)

---

## 1. IP 位址

### 127.0.0.1 — Loopback（只有自己看得到）

```
你的電腦
┌─────────────────────────────┐
│                             │
│   http://127.0.0.1:8001     │  ← 只有這台電腦自己可以連
│                             │
└─────────────────────────────┘
         ✗ 同事連不進來
```

`127.0.0.1` 又叫 loopback address，意思是「自己連自己」。
任何 request 都不會真的出去網路，直接在本機內部繞一圈回來。

**適合：本地開發，只有自己用**

---

### 0.0.0.0 — 監聽所有介面

```
你的電腦（或 Server）
┌─────────────────────────────┐
│                             │
│   API_HOST=0.0.0.0          │  ← 監聽所有網路介面
│                             │
│   192.168.x.x:8008  ✅      │  ← 同事從區網可以連
│   127.0.0.1:8008    ✅      │  ← 自己也可以連
│                             │
└─────────────────────────────┘
```

`0.0.0.0` 不是一個真實的 IP，而是一個特殊的設定，意思是：
「**監聽這台機器上所有的網路介面**」。

所以設成 `0.0.0.0` 之後，不管從哪個 IP 打進來，service 都會回應。

**適合：部署到 server，讓別人連進來**

---

### Server IP — 區網位址

```
同事的電腦                    Server
┌───────────────┐            ┌───────────────────────┐
│               │            │                       │
│ 瀏覽器輸入：  │  ────────► │  192.168.x.x:8008     │
│ 192.168.x.x   │            │  (API_HOST=0.0.0.0)   │
│ :8008/docs    │            │                       │
└───────────────┘            └───────────────────────┘
```

Server 的 IP 是它在區網（LAN）裡的位址，同事用這個 IP 就可以連進來。

**怎麼查 Server 的 IP：**

```bash
# Linux / macOS
ip addr show | grep "inet " | grep -v 127.0.0.1

# 或更簡單
hostname -I
```

---

### 三者對比

| 設定 | 誰可以連 | 適合場景 |
|------|---------|---------|
| `127.0.0.1` | 只有自己 | 本地開發 |
| `0.0.0.0` | 所有人（透過 server IP）| 部署到 server |
| `192.168.x.x`（指定 IP）| 只有從這個介面進來的 | 特殊情況 |

> **一句話記住：** 本地開發用 `127.0.0.1`，要讓別人連就用 `0.0.0.0`

---

## 2. Port 是什麼，怎麼查

### Port 的概念

同一台 server 可以同時跑很多個 service，port 就是用來區分「這個 request 要給哪個 service」的號碼。

```
Server 192.168.x.x
├── :8000  →  boltz2
├── :8002  →  同事 A 的 API
├── :8003  →  同事 B 的 API
├── :8008  →  你的 API          ← 這次 demo 用的
└── :8026  →  excipient pipeline
```

就像一棟大樓有很多房間，IP 是大樓地址，port 是房間號碼。

---

### 怎麼查哪些 port 已經被佔用

```bash
# 列出所有正在監聽的 port
ss -tlnp

# 只看數字，排序
ss -tlnp | awk 'NR>1 {print $4}' | grep -oP ':\K\d+' | sort -n

# 查 Docker container 的 port
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

**挑 port 的原則：**
- 避開常用的：`80`（HTTP）、`443`（HTTPS）、`22`（SSH）、`3306`（MySQL）
- 8000–9000 是常見的開發用 port
- 每個人用不同的 port，避免衝突（放在 `.env` 裡各自設定）

---

## 3. .env 檔案

### 為什麼要用 .env

直接把設定寫在 code 裡有幾個問題：

```python
# ❌ 不好的做法：設定寫死在 code 裡
uvicorn.run("app:app", host="192.168.66.188", port=8008)
```

- 換環境就要改 code
- Server IP 和 port 不小心就 commit 到 GitHub
- 每個人要用不同 port 時，大家都要改 code

`.env` 就是把這些「會因環境而變」的設定獨立出來：

```bash
# .env（不進 git）
API_HOST=0.0.0.0
API_PORT=8008
```

```python
# code 裡只讀環境變數（不寫死）
host = os.getenv("API_HOST", "127.0.0.1")
port = int(os.getenv("API_PORT", 8001))
```

---

### .env 使用流程

```bash
# 1. repo 裡有 .env.example（範本，有進 git）
cat .env.example
# API_HOST=0.0.0.0
# API_PORT=8007

# 2. 自己複製一份成 .env，然後修改
cp .env.example .env
# 編輯 .env，改成自己要用的 port

# 3. .env 不進 git（.gitignore 裡有設定）
cat .gitignore | grep env
# .env
```

> **原則：** `.env.example` 進 git 當範本，`.env` 不進 git 保護設定

---

### Docker 怎麼讀 .env

`docker-compose.yml` 裡有這一行：

```yaml
env_file:
  - .env
```

Docker 啟動 container 時會自動把 `.env` 裡的變數注入進去，
所以 code 裡的 `os.getenv("API_HOST")` 就能讀到 `0.0.0.0`。

---

## 4. Container 是什麼

### 沒有 Container 的問題

```
你的電腦                    同事的電腦
┌──────────────────┐        ┌──────────────────┐
│ Python 3.11      │        │ Python 3.8       │
│ fastapi 0.100    │        │ fastapi 0.95     │
│ numpy 1.24       │        │ numpy 1.21       │
│                  │        │                  │
│ ✅ 可以跑        │        │ ❌ 跑不起來      │
└──────────────────┘        └──────────────────┘
```

不同電腦的環境不一樣，同一份 code 跑出來的結果可能不同，
甚至根本跑不起來。

---

### Container 解決了什麼

```
Dockerfile（打包說明書）
┌─────────────────────────────────┐
│ FROM python:3.11-slim           │
│ COPY requirements.txt .         │
│ RUN pip install -r requirements │
│ COPY . .                        │
│ CMD uvicorn app.main:app        │
└─────────────────────────────────┘
         ↓  docker compose build
┌─────────────────────────────────┐
│ Container Image                 │
│ ┌───────────────────────────┐   │
│ │ Python 3.11               │   │
│ │ fastapi + 所有套件         │   │  ← 打包在一起
│ │ 你的 code                 │   │
│ └───────────────────────────┘   │
└─────────────────────────────────┘
         ↓  docker compose up
在任何有 Docker 的機器上跑 → 結果都一樣 ✅
```

**一句話：** Container 把 Python、套件、code 全部打包在一起，在哪台機器跑結果都一樣。

---

### Container vs 虛擬機（VM）

|  | VM | Container |
|--|----|----|
| 包含 | 整個作業系統 | 只有應用程式 + 套件 |
| 大小 | GB 級 | MB 級 |
| 啟動時間 | 分鐘 | 秒 |
| 適合 | 完整隔離環境 | 部署應用程式 |

---

## 5. Docker 常用指令速查

### 基本操作

```bash
# 建立 image（第一次 or 改了 code/requirements 後）
docker compose build

# 建立 image（強制不用 cache，確保最新）
docker compose build --no-cache

# 啟動 container（背景執行）
docker compose up -d

# 停止並移除 container
docker compose down

# 查看目前跑著的 container
docker ps

# 查看所有 container（包含已停止的）
docker ps -a
```

---

### 查看 log

```bash
# 查看 log（一次性）
docker compose logs api

# 即時追蹤 log（Ctrl+C 離開）
docker compose logs -f api

# 直接用 container name
docker logs -f advanced_structure-api-1
```

---

### 確認 service 有跑起來

```bash
# 看 log 裡有沒有這行
# Uvicorn running on http://0.0.0.0:8008

# 用 curl 測試
curl http://localhost:8008/
# → {"status": "running"}

# 看 port mapping
docker ps --format "table {{.Names}}\t{{.Ports}}"
# advanced_structure-api-1   0.0.0.0:8008->8008/tcp
```

---

### 常見問題排查

| 症狀 | 可能原因 | 解法 |
|------|---------|------|
| `Connection reset` | `API_HOST=127.0.0.1` | 改成 `0.0.0.0`，重啟 |
| Port 衝突 | 同個 port 已被佔用 | 改 `.env` 的 `API_PORT` |
| 改了 code 沒生效 | Image 沒重 build | `docker compose build && up -d` |
| Container 一直重啟 | 啟動時 error | `docker compose logs api` 看原因 |
| `image not found` | 還沒 build | `docker compose build` |

---

*有其他問題歡迎找我 👋*
