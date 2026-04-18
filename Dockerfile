# ================= FRONTEND BUILD =================
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Fix React + Node 18 issue
ENV NODE_OPTIONS=--openssl-legacy-provider
ENV NPM_CONFIG_AUDIT=false
ENV NPM_CONFIG_FUND=false

# Install dependencies
COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps --no-audit --no-fund

# Copy source and build
COPY frontend/ ./
RUN NODE_OPTIONS="--openssl-legacy-provider --max-old-space-size=4096" npm run build


# ================= BACKEND =================
FROM python:3.9-slim AS backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browser
RUN playwright install chromium

# Copy frontend build into backend static folder
COPY --from=frontend-builder /app/frontend/build ./static

# Copy backend code
COPY backend/ ./

# Create directory for generated pages
RUN mkdir -p generated_pages

ENV PYTHONPATH=/app
ENV GENERATED_PAGES_DIR=generated_pages

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]