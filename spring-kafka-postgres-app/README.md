# Base App: Spring Boot + Kafka + PostgreSQL + K8s + ArgoCD + OpenTelemetry

This folder contains a starter application and deployment manifests.

## Features
- Spring Boot REST API (`/api/events`)
- Kafka producer/consumer flow
- PostgreSQL persistence via Spring Data JPA
- OpenTelemetry tracing via OTLP exporter
- Kubernetes manifests (Kustomize base)
- ArgoCD `Application` manifest

## Local run
Prerequisites: Java 17+, Maven, Docker (or local Kafka/PostgreSQL).

```bash
cd spring-kafka-postgres-app
mvn spring-boot:run
```

Environment variables:
- `DB_URL` (default `jdbc:postgresql://localhost:5432/baseapp`)
- `DB_USERNAME` (default `baseapp`)
- `DB_PASSWORD` (default `baseapp`)
- `KAFKA_BOOTSTRAP_SERVERS` (default `localhost:9092`)
- `OTEL_EXPORTER_OTLP_ENDPOINT` (default `http://otel-collector:4318/v1/traces`)

## API
Create event:
```bash
curl -X POST http://localhost:8080/api/events \
  -H 'Content-Type: application/json' \
  -d '{"eventId":"evt-1","payload":"hello"}'
```

List persisted events:
```bash
curl http://localhost:8080/api/events
```

## Build image
```bash
docker build -t ghcr.io/your-org/baseapp:0.0.1 .
```

## Kubernetes deploy (manual)
```bash
kubectl apply -k k8s/base
```

## ArgoCD deploy
1. Update `argocd/application.yaml` with your Git repo URL/revision.
2. Apply:

```bash
kubectl apply -f argocd/application.yaml
```
