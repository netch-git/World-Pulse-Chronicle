FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies required by pandas/yfinance
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (supports building from project root or backend/ directory)
COPY backend/requirements.txt* requirements.txt* ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy full project context so both backend/main.py and frontend/index.html are present
COPY . /app

EXPOSE 8080

CMD ["sh", "-c", "if [ -f backend/main.py ]; then exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1; else exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1; fi"]
