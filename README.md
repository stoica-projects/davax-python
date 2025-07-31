# Math Microservice

A simple, production‑ready microservice for solving mathematical operations including:

- Exponentiation (`pow`)
- N‑th Fibonacci number (`fib`)
- Factorial (`fact`)

Built with FastAPI, SQLite (async), Pydantic settings, Click for CLI, caching, authentication, structured logging, and Prometheus monitoring.

---

## Table of Contents

1. [Features](#features)
2. [Architecture & Design](#architecture--design)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Running the Service](#running-the-service)
7. [API Usage](#api-usage)
8. [CLI Usage](#cli-usage)
9. [Testing & Linting](#testing--linting)
10. [Project Structure](#project-structure)
11. [Containerization & Deployment](#containerization--deployment)

---

## Features

- **Three mathematical operations**: `pow`, `fib`, `fact` exposed via HTTP REST API
- **Persistent request logging**: All API calls are saved to a SQLite database (`request_logs` table)
- **Dictionary‑based caching**: In‑memory caching for repeated operations (via `lru_cache`)
- **Authentication**: Simple token‑based header (`X-API-Token`) to secure endpoints
- **Structured logging**: JSON logs emitted with `structlog`
- **Monitoring**: Prometheus metrics exposed on `/metrics` (via `prometheus-fastapi-instrumentator`)

---

## Architecture & Design

- **Framework**: FastAPI (async) for high performance and automatic docs
- **ORM**: SQLAlchemy 2 (async) with SQLite (`aiosqlite` driver)
- **Validation**: Pydantic v2 + `pydantic-settings` for environment config
- **CLI**: `click` to provide a local command‑line interface for quick operations
- **Caching**: `functools.lru_cache` for Fibonacci and optional dict‑based patterns
- **Auth**: FastAPI `APIKeyHeader` dependency (`X-API-Token`)
- **Logging**: `structlog` for JSON‑structured logs
- **Metrics**: `prometheus-fastapi-instrumentator` for HTTP metrics, latency, error rates

---

## Prerequisites

- Python 3.13
- `git`
- (Optional) virtual environment tool (venv)

---

## Installation

```bash
# Clone repository
git clone <repo_url> math_service
cd math_service

# Create virtual environment (Windows / PowerShell)
py -3.13 -m venv .venv

# Activate environment (PowerShell)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force
. .\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

---

## Configuration

Environment variables are loaded from `.env` (create from `.env.example`):

```dotenv
API_TOKEN=topsecret            # token for X-API-Token
DATABASE_URL=sqlite+aiosqlite:///./requests.db
LOG_LEVEL=INFO
PROMETHEUS_ENABLED=true
```

Copy and edit:

```bash
cp .env.example .env
```

---

## Running the Service

Start the API server:

```bash
uvicorn app.main:app --reload
```

- **Swagger UI**: http://127.0.0.1:8000/docs
- **Metrics**: http://127.0.0.1:8000/metrics

Stop server: `Ctrl+C`

---

## API Usage

All endpoints require header `X-API-Token: <your_token>`.

### 1. Power

```http
POST /math/pow HTTP/1.1
Content-Type: application/json
X-API-Token: topsecret

{"base": 2, "exponent": 8}
```
**Response**:
```json
{"result":"256"}
```

### 2. Fibonacci

```http
POST /math/fib HTTP/1.1
Content-Type: application/json
X-API-Token: topsecret

{"n": 10}
```
**Response**:
```json
{"result":"55"}
```

### 3. Factorial

```http
POST /math/fact HTTP/1.1
Content-Type: application/json
X-API-Token: topsecret

{"n": 5}
```
**Response**:
```json
{"result":"120"}
```

---

## CLI Usage

```bash
# Ensure server running
env> python cli.py pow 2 10   # => 1024
env> python cli.py fib 12      # => 144
env> python cli.py fact 6      # => 720
```

---

## Testing & Linting

```bash
# Run tests
pytest -q

# Lint code
flake8
```

---

## Project Structure

```
math_service/
├── app/
│   ├── main.py          # FastAPI app instantiation
│   ├── config.py        # Environment settings loader
│   ├── logging_conf.py  # Structured logging config
│   ├── auth.py          # API token dependency
│   ├── db.py            # AsyncSession factory
│   ├── models.py        # SQLAlchemy ORM definitions
│   ├── schemas.py       # Pydantic models
│   ├── crud.py          # Database operations
│   ├── utils.py         # Math logic + caching
│   └── api.py           # API router & endpoints
├── cli.py               # Command-line client
├── .env.example         # Example environment variables
├── requirements.txt     # Dependency pins
├── .flake8              # Lint rules
├── tests/               # Test suite
└── requests.db          # SQLite database file (auto-created)
```


---
## Containerization & Deployment

### 1. Building the Docker image

> **Rancher Desktop** runs the **containerd** runtime and ships with the `nerdctl` CLI (Docker‑compatible).

```bash
# From project root (where Dockerfile lives)
nerdctl --namespace k8s.io build -t math-svc:0.1.0 .
```

* `--namespace k8s.io` puts the image in the same containerd namespace that Kubernetes uses, so Pods can use it without pulling from an external registry.  
* Verify the image: `nerdctl --namespace k8s.io images`

### 2. Local test (optional, outside K8s)

```bash
nerdctl run -p 8000:8000 --name math math-svc:0.1.0
# Browse http://localhost:8000/docs
```

### 3. Kubernetes manifests

All YAML files live under **`deploy/`**:

```
deploy/
├─ namespace.yaml    # Namespace “math”
├─ secret.yaml       # API_TOKEN, DATABASE_URL, …
├─ deployment.yaml   # 2 replicas, imagePullPolicy: IfNotPresent
├─ service.yaml      # ClusterIP on port 80 → 8000
└─ ingress.yaml      # (optional) host math.local → service
```

Apply:

```bash
kubectl apply -f deploy/namespace.yaml      # once
kubectl apply -f deploy/                    # rest
```

Check resources:

```bash
kubectl -n math get pods
kubectl -n math get svc,ingress
```

Port‑forward shortcut (if no Ingress):

```bash
kubectl -n math port-forward svc/math-svc 8000:80
```

### 4. Observability

The `prometheus-fastapi-instrumentator` exposes `/metrics`; if running Prometheus Operator, add a **ServiceMonitor** (example under `deploy/monitoring/`).

### 5. Production vs. local

| Aspect | Local (demo) | Production recommendation |
|--------|--------------|---------------------------|
| Image | `math-svc:0.1.0` local | Push to a registry (GHCR, ECR, ACR) and update `image:` |
| DB | `emptyDir` + SQLite | PVC or external PostgreSQL |
| Scaling | `replicas: 2` | HPA + probes (already included) |
| Logs | JSON to stdout | Routed by Rancher stacks or shipped to Kafka/Loki |

> **TL;DR**: run `nerdctl build`, apply YAMLs, and the service is live in Rancher Desktop — containerized, authenticated, and monitored.

