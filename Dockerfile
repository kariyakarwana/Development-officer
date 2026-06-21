FROM python:3.11-slim

# Prevent buffering for clear log monitoring logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Pull dependencies system libraries for building psycopg2 if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 1111

# Run with Gunicorn on production port 1111
CMD ["gunicorn", "--bind", "0.0.0.0:1111", "app:app"]