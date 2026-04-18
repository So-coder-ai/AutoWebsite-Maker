# Backend-only image (API + Playwright). Build context must be ./backend
# For Render all-in-one (React UI + API), use the repo root Dockerfile instead.
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browser (IMPORTANT for your scraper)
RUN playwright install chromium

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p generated_pages uploads

ENV PYTHONPATH=/app
ENV GENERATED_PAGES_DIR=generated_pages

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]