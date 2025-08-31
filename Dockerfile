
FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port for Render
EXPOSE 8000

# Use gunicorn for production ASGI deployment
CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
