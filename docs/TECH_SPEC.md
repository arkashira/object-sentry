# TECH_SPEC.md – Object Sentry  

**Version:** 1.0.0  
**Author:** Axentx OS – Senior Product/Engineering Lead  
**Date:** 2026‑06‑25  

---  

## 1. Overview  

Object Sentry is a self‑contained platform that receives image or video files, validates their format, stores the raw assets, runs a high‑performance object‑detection model, and returns structured detection results. It is exposed as a **RESTful HTTP API** and also provides a **CLI entry‑point** (`python -m src.object_sentry`) for quick local testing.  

The service is designed for:

| Goal | Implementation |
|------|----------------|
| **Low latency inference** | GPU‑accelerated PyTorch model (YOLOv8‑nano) served via `vLLM`‑compatible inference wrapper. |
| **Scalable ingestion** | Asynchronous task queue (Celery + Redis) decouples upload from inference. |
| **Robust validation** | MIME‑type and file‑signature checks; size limits configurable per tenant. |
| **Audit‑ready storage** | Raw files stored in an S3‑compatible bucket; metadata persisted in PostgreSQL. |
| **Observability** | OpenTelemetry tracing, Prometheus metrics, structured logs (JSON). |
| **CI/CD‑ready** | Docker‑based builds, Helm chart for Kubernetes, automated tests (pytest). |

---  

## 2. Architecture Diagram  

```
+-------------------+        +-------------------+        +-------------------+
|   Client (Web /   |  HTTP  |   API Gateway     |  gRPC  |   Inference       |
|   Mobile / CLI)  |------->| (FastAPI + uvicorn) |----->|   Service         |
+-------------------+        +-------------------+        +-------------------+
                                   |   ^   |
                                   |   |   |   (async task)
                                   v   |   |
                           +-------------------+        +-------------------+
                           |   Task Queue      |<------>|   Worker (Celery)|
                           |   (Redis)         |        |   (GPU)          |
                           +-------------------+        +-------------------+
                                   |   ^
                                   |   |   (metadata)
                                   v   |
                           +-------------------+
                           |   PostgreSQL      |
                           |   (metadata)     |
                           +-------------------+
                                   |
                                   v
                           +-------------------+
                           |   Object Store    |
                           |   (MinIO / S3)    |
                           +-------------------+
```

---  

## 3. Core Components  

| Component | Responsibility | Implementation Details |
|-----------|----------------|------------------------|
| **API Layer** | HTTP endpoint handling, request validation, auth (optional), response formatting. | FastAPI (Python 3.11), Pydantic models, uvicorn workers (4 × CPU). |
| **CLI Wrapper** | Thin wrapper around the API for local dev / ad‑hoc usage. | `src/object_sentry/__main__.py` uses `argparse` → internal client library. |
| **Task Queue** | Decouple upload from heavy inference, enable horizontal scaling. | Celery 5.x with Redis 7 as broker & result backend. |
| **Worker** | Pull tasks, download raw file from object store, run detection, write results. | Python worker process pinned to a GPU node, uses PyTorch 2.3, YOLOv8‑nano (ONNX runtime optional). |
| **Model Server** | Optional hot‑swap inference service (exposed via gRPC). | `vLLM`‑compatible wrapper (future‑proof for LLM‑based vision models). |
| **Metadata Store** | Persist detection jobs, file metadata, results, audit logs. | PostgreSQL 15, SQLAlchemy 2 ORM, Alembic migrations. |
| **Object Store** | Durable storage for raw uploads and optional processed assets. | MinIO (self‑hosted) or AWS S3 (via `boto3`). |
| **Observability** | Tracing, metrics, logs. | OpenTelemetry SDK → Jaeger, Prometheus exporter, JSON logs via `structlog`. |
| **CI/CD Pipeline** | Lint, test, build, push Docker image, Helm release. | GitHub Actions, `pytest`, `ruff`, `mypy`, Docker BuildKit, Helm 3. |

---  

## 4. Data Model  

### 4.1 Database Schema (PostgreSQL)

| Table | Columns | Description |
|-------|---------|-------------|
| `files` | `id` (UUID PK), `filename` (TEXT), `content_type` (TEXT), `size_bytes` (BIGINT), `bucket_key` (TEXT), `uploaded_at` (TIMESTAMP), `status` (ENUM: `PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`) | Raw asset metadata. |
| `detections` | `id` (UUID PK), `file_id` (FK → `files.id`), `model_version` (TEXT), `detected_at` (TIMESTAMP), `result_json` (JSONB) | One‑to‑many: a file can have multiple detection runs (e.g., re‑run with newer model). |
| `audit_logs` | `id` (UUID PK), `event_type` (TEXT), `payload` (JSONB), `created_at` (
