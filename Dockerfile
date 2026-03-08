FROM node:20-slim AS frontend-builder

WORKDIR /frontend
COPY frontend/package.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

WORKDIR /app

COPY . .
COPY --from=frontend-builder /frontend/dist/assets /app/gexable_esg/apps/django_project/core_api/static/core_api/frontend/assets

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir . psycopg2-binary

EXPOSE 8000

CMD ["sh", "gexable_esg/apps/django_project/scripts/bootstrap_runtime.sh"]
