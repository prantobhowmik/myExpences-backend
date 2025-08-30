FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000

CMD ["watchmedo", "auto-restart", "--directory=.", "--pattern=*.py", "--recursive", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
