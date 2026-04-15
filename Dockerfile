# Multi-stage build for unified deployment
FROM node:16-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install frontend dependencies with legacy peer deps
RUN npm install --legacy-peer-deps

# Copy frontend source code
COPY frontend/ ./

# Build frontend with OpenSSL legacy provider
RUN NODE_OPTIONS="--openssl-legacy-provider" npm run build

# Python backend stage
FROM python:3.9-slim AS backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/build ./static

# Copy backend source code
COPY backend/ ./

# Create necessary directories
RUN mkdir -p generated_pages

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV GENERATED_PAGES_DIR=generated_pages

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
