# ROADMAP.md – Object Sentry

## Vision
Create a reliable, easy‑to‑integrate platform that delivers high‑accuracy object detection for images and videos, with a focus on developer experience, scalability, and extensible model support.

---

## Milestones Overview

| Milestone | Target Date | Description | MVP‑Critical |
|-----------|-------------|-------------|--------------|
| **MVP (Launch)** | **2026‑09‑30** | Core detection service for single‑image uploads, basic validation, REST API, CI/CD pipeline, automated tests, and Docker container. | ✅ |
| **v1.0 – Multi‑Media & Edge** | 2026‑12‑15 | Video stream support, batch processing, model zoo (YOLOv8, EfficientDet), GPU acceleration, monitoring dashboard. | – |
| **v2.0 – Enterprise & Extensibility** | 2027‑04‑30 | On‑prem/k8s deployment, plug‑in architecture for custom models, RBAC & audit logging, SLA‑grade performance, SDKs for Python/JS/Go. | – |

---

## MVP – Must‑Have for Launch (✅)

| Feature | Acceptance Criteria | Owner |
|---------|----------------------|-------|
| **CLI / Python entry‑point** | `python -m src.object_sentry --filename <path> --content-type <mime>` runs end‑to‑end detection and returns JSON with bounding boxes. | Lead Engineer |
| **File validation** | Reject unsupported formats with clear error (`400 Bad Request`). Supported: JPEG, PNG, MP4 (future). | QA |
| **Single‑image detection** | Integrate a pre‑trained YOLOv8 model; ≥ 70 % mAP on COCO validation set. | ML Engineer |
| **REST API** | `POST /detect` accepts multipart/form‑data, returns `{objects: [{label, confidence, box}]}`. | Backend |
| **Docker image** | `docker pull axentx/object-sentry:latest` runs the service with one‑click start. | DevOps |
| **Automated test suite** | ≥ 90 % coverage; includes unit, integration, and contract tests (`pytest`). | QA |
| **CI/CD pipeline** | GitHub Actions: lint → test → build → push Docker on `main` merge. | DevOps |
| **Documentation** | README with quick‑start, API spec (OpenAPI), and contribution guide. | Technical Writer |
| **Monitoring stub** | Basic health endpoint (`/healthz`) and logs to stdout (JSON format). | SRE |

*All MVP items are required for a production‑ready launch and will be gated by the Reviewer role.*

---

## v1.0 – Multi‑Media & Edge (Themes)

1. **Video & Batch Processing**  
   - `POST /detect/video` streams frames, returns per‑frame detections.  
   - Batch endpoint for multiple images in a single request.  

2. **Model Zoo & GPU Acceleration**  
   - Add EfficientDet and MobileNet‑SSD models.  
   - Enable optional CUDA / TensorRT inference paths.  

3. **Observability Dashboard**  
   - Grafana + Prometheus stack exposing request latency, throughput, and error rates.  

4. **Rate Limiting & Auth**  
   - API key system with per‑key quota.  
   - Simple OAuth2 bearer token support.  

5. **Packaging Enhancements**  
   - Helm chart for Kubernetes deployment.  
   - Multi‑arch Docker images (amd64/arm64).  

*Deliverables are shippable as a single release tag `v1.0.0`.*

---

## v2.0 – Enterprise & Extensibility (Themes)

1. **Plug‑in Architecture**  
   - SDK for custom model registration (Python class interface).  
   - Model versioning and A/B testing framework.  

2. **Enterprise Deployment Options**  
   - On‑prem installer (Ansible).  
   - Managed Helm chart with auto‑scaling policies.  

3. **Security & Governance**  
   - Role‑Based Access Control (RBAC) integrated with LDAP/OIDC.  
   - Immutable audit log stored in Cloud‑native object store.  

4. **SLA & Performance Guarantees**  
   - Benchmark suite to certify ≤ 100 ms latency for 1080p video on V100.  
   - Auto‑fallback to CPU inference when GPU unavailable.  

5. **SDKs & Language Bindings**  
   - Official client libraries for Python, JavaScript (Node), and Go.  
   - Typed OpenAPI spec generation.  

*Target release tag `v2.0.0` with full enterprise‑grade documentation.*

---

## Release Process

1. **Feature Freeze** – Two weeks before each target date.  
2. **Beta Testing** – Internal QA + selected external partners (invite‑only).  
3. **Staging Deployment** – Full CI pipeline runs against staging environment.  
4. **Production Roll‑out** – Blue‑green deployment with health checks; rollback window 24 h.  

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Model accuracy drift | ↓ user trust | Continuous evaluation pipeline; auto‑retrain schedule. |
| GPU resource contention | Performance bottleneck | Autoscaling policies; fallback CPU path. |
| Security breach via file upload | Data leak | Strict MIME/type validation; sandboxed processing. |
| Dependency licensing (e.g., YOLO weights) | Legal | Use permissively‑licensed checkpoints; maintain SPDX manifest. |

---

## Success Metrics (Post‑Launch)

- **Adoption**: ≥ 500 active API keys within 3 months.  
- **Reliability**: 99.9 % uptime, 95 th percentile latency ≤ 150 ms (image).  
- **Accuracy**: Maintain ≥ 70 % mAP on user‑submitted data (quarterly audit).  
- **Revenue**: $10k MRR from paid API usage by Q2 2027.  

--- 

*Prepared by the Object Sentry product team, aligned with AXENTX OS standards.*
