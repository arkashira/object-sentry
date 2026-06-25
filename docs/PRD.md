# 📄 Product Requirements Document (PRD)  
**Project:** Object Sentry  
**Owner:** Senior Product/Engineering Lead – Axentx OS  
**Date:** 2026‑06‑25  

---

## 1. Problem Statement  

Enterprises and developers increasingly need **reliable, low‑latency object detection** for images and video streams (e.g., security footage, retail analytics, autonomous robotics). Existing SaaS offerings are either:

* **Expensive** per‑image pricing models that don’t scale for high‑volume workloads.  
* **Opaque** black‑box APIs lacking on‑premise deployment options for data‑privacy‑sensitive customers.  
* **Hard to integrate** – requiring custom wrappers, complex authentication, and limited format validation.

**Result:** Teams spend weeks building glue code, incur unpredictable costs, and risk non‑compliance with data‑privacy regulations.

---

## 2. Target Users  

| Segment | Persona | Primary Pain | Desired Outcome |
|---------|---------|--------------|-----------------|
| **AI‑Enabled Product Teams** | *ML Engineer* | Need a plug‑and‑play detection service that can run on‑prem or in the cloud, with deterministic pricing. | One‑command inference with built‑in validation, easy CI/CD integration. |
| **Security & Surveillance Vendors** | *Systems Integrator* | Must process video streams in real‑time while guaranteeing data never leaves the customer’s network. | Deployable container that runs locally, supports batch/video ingestion, and returns detections instantly. |
| **Retail & Analytics Startups** | *Data Analyst* | Require quick prototyping on image datasets without managing model infrastructure. | Simple CLI / Python SDK, auto‑download of optimized models, clear error messages on bad inputs. |

---

## 3. Goals & Success Metrics  

| Goal | Metric (Target) | Measurement Cadence |
|------|----------------|---------------------|
| **G1 – High‑accuracy detection** | Mean Average Precision (mAP) ≥ 0.78 on COCO‑val (baseline model) | Quarterly benchmark |
| **G2 – Low latency** | 95 % of inference calls ≤ 120 ms for 720p video frame on a single V100 GPU | Continuous CI performance tests |
| **G3 – Seamless integration** | 0 % of CI pipeline failures due to missing dependencies for new customers | Post‑deployment monitoring (first 30 days) |
| **G4 – Data‑privacy compliance** | 100 % of deployments can run fully offline (no external network calls) | Security audit (annual) |
| **G5 – Commercial traction** | 5 paying pilot customers within 3 months of GA | Sales pipeline tracking |

---

## 4. Scope  

### In‑Scope (Must‑Have)

1. **CLI Entrypoint** – `python -m src.object_sentry --filename <path> --content-type <mime>`  
   * Validates file existence, MIME type, and size (≤ 50 MB).  
   * Returns JSON payload with detected objects (class, confidence, bounding box).

2. **Python SDK** – `object_sentry.detect(file_path, content_type)` wrapper exposing same functionality programmatically.

3. **Model Bundle** – Pre‑trained, quantized YOLO‑v8 (or equivalent) optimized for CPU & GPU inference via **vLLM** backend.

4. **Container Image** – Dockerfile producing a lightweight (≈ 300 MB) image with:
   * OS‑level security (non‑root user, read‑only filesystem).  
   * No outbound network calls by default.

5. **Test Suite** – PyTest coverage ≥ 90 % covering:
   * File validation edge cases (unsupported MIME, corrupted files).  
   * Correct JSON schema of detection results.  
   * Performance regression (latency thresholds).

6. **Documentation** – README, API reference, quick‑start guide, and CI/CD integration examples.

### Out‑of‑Scope (Nice‑to‑Have)

| Feature | Reason |
|---------|--------|
| **Real‑time video streaming API** | Requires separate streaming ingest service; slated for Phase 2. |
| **Custom model training UI** | Complex product; will be offered as a separate “Model Studio” service. |
| **Edge‑device (ARM) binaries** | Current focus on x86_64 containers; ARM support planned after market validation. |
| **Marketplace billing integration** | Pricing model to be defined after pilot revenue validation. |

---

## 5. Key Features (Prioritized)

| Priority | Feature | Description | Acceptance Criteria |
|----------|---------|-------------|----------------------|
| **P1** | **Robust Input Validation** | Detect unsupported formats, oversized files, and corrupted payloads before inference. | - Returns HTTP 400 / CLI error with clear message for each invalid case.<br>- Logs validation failures with request ID. |
| **P1** | **Fast Inference Engine** | Leverage **vLLM** for batched, low‑latency inference on both CPU and GPU. | - 95 % of calls ≤ 120 ms on V100 for 720p frame.<br>- Fallback to CPU with ≤ 300 ms latency. |
| **P1** | **Standardized JSON Output** | Consistent schema: `{objects: [{label, confidence, bbox:[x1,y1,x2,y2]}]}`. | - Schema validated by JSON‑Schema test.<br>- Includes deterministic ordering (by confidence desc). |
| **P2** | **Dockerized Deployment** | One‑click container that runs offline, exposing a REST endpoint (`/detect`). | - Container builds in < 5 min.<br>- No outbound network traffic on start. |
| **P2** | **Python SDK** | Thin wrapper around CLI / REST, pip‑installable. | - `pip install object-sentry` succeeds.<br>- SDK raises `ObjectSentryError` with same messages as CLI. |
| **P3** | **Batch Processing** | Accept a list of file paths for bulk detection. | - Returns array of detection results preserving input order.<br>- Batch latency ≤ 1.2× single‑image latency per image. |
| **P3** | **Telemetry & Logging** | Emit structured logs (JSON) with request ID, latency, model version. | - Logs ingested by standard ELK stack without modification.<br>- No PII leakage. |

---

## 6. Success Metrics (Detailed)

| Metric | Definition | Target | Data Source |
|--------|------------|--------|-------------|
| **Detection Accuracy** | mAP on COCO‑val using shipped model | ≥ 0.78 | Automated benchmark script (run nightly) |
| **Inference Latency** | 95th percentile response time per image | ≤ 120 ms (GPU) / ≤ 300 ms (CPU) | CI performance test, production monitoring |
| **Error Rate** | % of API calls returning validation errors (should be user‑error, not system) | ≤ 2 % (mostly due to bad inputs) | Logs aggregation |
| **Adoption** | Number of unique API keys issued | ≥ 5 paid pilots in 90 days | Billing system |
| **Reliability** | Uptime of containerized service (excluding customer infra) | 99.9 % | Health‑check endpoint |

---

## 7. Milestones & Timeline  

| Milestone | Deliverable | Owner | Due |
|-----------|-------------|-------|-----|
| **M1 – Foundations** | Repo scaffold, CI pipeline, unit tests (90 % coverage) | Lead Engineer | 2026‑07‑05 |
| **M2 – Core Engine** | vLLM integration, model loading, CLI detection | ML Engineer | 2026‑07‑19 |
| **M3 – Validation & Output** | Input validation, JSON schema, error handling | Backend Engineer | 2026‑07‑26 |
| **M4 – Containerization** | Dockerfile, offline mode, health endpoint | DevOps Engineer | 2026‑08‑02 |
| **M5 – SDK & Docs** | pip package, quick‑start guide, API reference | Docs Engineer | 2026‑08‑09 |
| **M6 – Beta Release** | Public beta on internal marketplace, pilot onboarding | PM / Sales | 2026‑08‑23 |
| **M7 – GA Launch** | Version 1.0.0, SLA, support hand‑off | PM | 2026‑09‑15 |

---

## 8. Risks & Mitigations  

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Model performance degradation on unseen domains** | Lower accuracy → customer churn | Medium | Provide domain‑specific fine‑tuning guide; collect feedback for future model updates. |
| **Heavy GPU cost for customers** | Adoption barrier | Low | Offer CPU‑only fallback; ship quantized model to reduce memory/compute. |
| **Regulatory compliance (data residency)** | Blocking sales in certain regions | Low | Offline container ensures data never leaves premises; provide audit logs. |
| **Dependency drift (vLLM updates)** | Breakage in CI/production | Medium | Pin vLLM version, run weekly dependency audit, automated compatibility tests. |

---

## 9. Open Questions  

1. **Pricing Model:** Usage‑based (per‑image) vs. subscription for container license?  
2. **Model Refresh Cadence:** Quarterly vs. on‑demand?  
3. **Support SLA Levels:** Tiered support for enterprise vs. self‑service?  

*Answers to be decided post‑pilot validation.*

---

## 10. Approvals  

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner |  |  |  |
| Engineering Lead |  |  |  |
| QA Lead |  |  |  |
| Legal / Compliance |  |  |  |

--- 

*Prepared by the Object Sentry product team. This document is the single source of truth for the development, testing, and launch of the Object Sentry platform.*
