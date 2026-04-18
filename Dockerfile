FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

ENV NODE_OPTIONS=--openssl-legacy-provider
ENV NPM_CONFIG_AUDIT=false
ENV NPM_CONFIG_FUND=false

COPY frontend/package*.json ./

RUN npm install --legacy-peer-deps --no-audit --no-fund

COPY frontend/ ./

RUN npm run build

FROM python:3.9-slim AS backend

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium

COPY --from=frontend-builder /app/frontend/build ./static

COPY backend/ ./

RUN mkdir -p generated_pages

EXPOSE 8000

ENV PYTHONPATH=/app
ENV GENERATED_PAGES_DIR=generated_pages
ENV PORT=8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
