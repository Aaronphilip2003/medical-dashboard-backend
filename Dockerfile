# Use Python 3.11 as base (to ensure compatibility with your newer package versions)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install gunicorn
RUN pip install gunicorn

# Updated command to use gunicorn
CMD exec gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind :$PORT 