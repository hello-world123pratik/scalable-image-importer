# Use official Python slim image
FROM python:3.12-slim

# -------------------------------------------------
# Environment variables
# -------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=api.settings

# -------------------------------------------------
# System dependencies
# -------------------------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------
# Working directory
# -------------------------------------------------
WORKDIR /app

# -------------------------------------------------
# Install Python dependencies
# -------------------------------------------------
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -------------------------------------------------
# Copy project files
# -------------------------------------------------
COPY . .

# -------------------------------------------------
# Collect static files (won't fail container if missing)
# -------------------------------------------------
RUN python manage.py collectstatic --noinput || true

# -------------------------------------------------
# Expose port
# -------------------------------------------------
EXPOSE 8000

# -------------------------------------------------
# Run server
# -------------------------------------------------
CMD python manage.py migrate --noinput && \
    gunicorn api.wsgi:application --bind 0.0.0.0:8000

