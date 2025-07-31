# ===============================
# Stage de build (opțional)
# ===============================
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# Stage final – imagine ultra-light
# ===============================
FROM base AS final
COPY . .

# Uvicorn rulează un singur worker;
# la nivel de K8s te scalezi cu mai multe pod-uri.
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
