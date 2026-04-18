# Same as repo root Dockerfile; use when build context is ./backend (CI tools).
# Default Render deploy: use root Dockerfile with context ".".
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium

COPY . .

RUN mkdir -p generated_pages uploads

ENV PYTHONPATH=/app
ENV GENERATED_PAGES_DIR=generated_pages

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
