# Dataflow Architecture
## Overview
The object-sentry dataflow architecture is designed to efficiently process and analyze computer vision data. The system consists of several tiers, each responsible for a specific function in the data processing pipeline.

## Dataflow Diagram
```
                                      +---------------+
                                      |  External    |
                                      |  Data Sources  |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      | Ingestion Layer  |
                                      |  (API Gateway,  |
                                      |   Load Balancer) |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      | Processing/    |
                                      | Transform Layer |
                                      |  (Worker Nodes,  |
                                      |   CV Frameworks) |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      | Storage Tier    |
                                      |  (Object Store,  |
                                      |   Database)      |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      | Query/Serving  |
                                      |  Layer (API     |
                                      |   Gateway, Cache) |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      | Egress to User  |
                                      |  (Client-Side    |
                                      |   Applications)  |
                                      +---------------+
```

## Components per Tier
* **External Data Sources**
  + Public datasets (e.g. ImageNet, COCO)
  + User-uploaded images and videos
  + IoT devices (e.g. cameras, sensors)
* **Ingestion Layer**
  + API Gateway (e.g. NGINX, Amazon API Gateway)
  + Load Balancer (e.g. HAProxy, Amazon ELB)
  + Authentication Service (e.g. OAuth, OpenID Connect)
* **Processing/Transform Layer**
  + Worker Nodes (e.g. Docker containers, Kubernetes pods)
  + Computer Vision Frameworks (e.g. OpenCV, TensorFlow)
  + Model Serving (e.g. TensorFlow Serving, AWS SageMaker)
* **Storage Tier**
  + Object Store (e.g. Amazon S3, Google Cloud Storage)
  + Database (e.g. MySQL, PostgreSQL)
  + Data Warehouse (e.g. Amazon Redshift, Google BigQuery)
* **Query/Serving Layer**
  + API Gateway (e.g. NGINX, Amazon API Gateway)
  + Cache (e.g. Redis, Memcached)
  + Query Engine (e.g. Apache Spark, Apache Flink)
* **Egress to User**
  + Client-Side Applications (e.g. web, mobile, desktop)
  + Webhooks (e.g. Slack, email notifications)

## Auth Boundaries
* **Ingestion Layer**: Authentication Service (e.g. OAuth, OpenID Connect) verifies user identity and authorizes access to the system.
* **Processing/Transform Layer**: Worker Nodes and Model Serving components are isolated from the public internet and only accessible through the Ingestion Layer.
* **Storage Tier**: Access to the Object Store and Database is restricted to authorized components within the system.
* **Query/Serving Layer**: API Gateway and Cache are configured to only serve authorized requests from the Egress to User tier.