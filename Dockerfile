# Python backend deployment
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

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
