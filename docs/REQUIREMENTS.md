# Requirements.md – Object Sentry

## 1. Functional Requirements

**FR-1** – The platform shall be invokable via the command line:
```
python -m src.object_sentry --filename <path> --content-type <mime>
```
where `--filename` specifies the path to an image or video file and `--content-type` specifies its MIME type.

**FR-2** – The platform shall verify that the file referenced by `--filename` exists, is readable, and is not a directory.

**FR-3** – The platform shall validate the `--content-type` against an allow‑list of MIME types:
- `image/jpeg`
- `image/png`
- `video/mp4`
If the supplied MIME type is not in the allow‑list, the platform shall print an error message to `stderr` and exit with a non‑zero status code.

**FR-4** – Upon successful validation, the platform shall read the file’s binary contents and upload it to a configurable storage backend (e.g., local `uploads/` directory or an S3‑compatible bucket). The upload location shall be configurable via the environment variable `OBJECT_SENTRY_UPLOAD_DIR` (default: `./uploads/`).

**FR-5** – After upload, the platform shall run an object‑detection model on the file and produce a list of detections, each containing:
- `label` (string)
- `confidence` (float, 0.0–1.0)
- `bbox` (list of four numbers: `[x_min, y_min, x_max, y_max]` for images; for video, per‑frame bounding boxes)

**FR-6** – The platform shall output the detection results as a JSON array to `stdout`. Example for an image:
```json
[
  {"label": "person", "confidence": 0.93, "bbox": [120, 85, 340, 420]},
  {"label": "dog",    "confidence": 0.78, "bbox": [500, 200, 620, 350]}
]
```
For video input, the JSON shall contain an outer array where each element corresponds to a frame index.

**FR-7** – The platform shall emit structured log messages (timestamp, level, component) to `stderr` using the standard Python `logging` module. Log level shall be controllable via the environment variable `OBJECT_SENTRY_LOG_LEVEL` (default: `INFO`).

**FR-8** – The platform shall support an optional `--output <path>` argument to write the JSON result to a file instead of `stdout`.

**FR-9** – The platform shall enforce a maximum file size (configurable via `OBJECT_SENTRY_MAX_SIZE_MB`, default `25 MB`). Files exceeding this limit shall trigger an error and non‑zero exit.

**FR-10** – The platform shall clean up temporary files created during processing (e.g., downloaded copies) upon completion or on error.

## 2. Non‑Functional Requirements

### 2.1 Performance
- **PF-1** – For JPEG/PNG images ≤ 5 MB, end‑to‑end latency (validation → upload → detection → output) shall be ≤ 2 seconds on a reference CPU (Intel i7‑12700K, 8 GB RAM).
- **PF-2** – For MP4 videos ≤ 50 MB and ≤ 30 seconds duration, average processing latency per frame shall be ≤ 0.05 seconds (20 fps) on the same reference hardware.
- **PF-3** – The platform shall be able to process at least 10 concurrent requests without degrading latency beyond 50 % of the single‑request baseline (horizontal scaling via multiple processes is allowed).

### 2.2 Security
- **SF-1** – All file‑system paths derived from `--filename` shall be sanitized to prevent directory‑traversal attacks (e.g., `../../etc/passwd`).
- **SF-2** – Uploaded files shall be stored with random, unpredictable names to avoid overwriting or guessing existing files.
- **SF-3** – The platform shall not execute any code contained in the uploaded file; it shall treat the file as opaque binary data only.
- **SF-4** – All external service calls (e.g., to S3) shall use TLS and be authenticated via IAM roles or access keys
