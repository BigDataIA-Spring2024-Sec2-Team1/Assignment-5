FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --use-deprecated=legacy-resolver -r /app/requirements.txt

COPY ./ /app/backend/

EXPOSE 8000

CMD ["uvicorn", "backend.src.main:app", "--log-config", "/app/backend/logging.conf", "--host", "0.0.0.0", "--port", "8000", "--reload"]
 