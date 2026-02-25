FROM python:3.12-slim

# Variables para que uv no cree un .venv dentro del contenedor
ENV UV_SYSTEM_PYTHON=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir uv

WORKDIR /app

# Copiamos solo el archivo de configuración primero
COPY pyproject.toml .

# Instalamos las dependencias directamente en el Python del sistema del contenedor
# --no-install-project evita que busque el backend 'hatchling'
RUN uv pip install -r pyproject.toml --system

# Ahora sí, copiamos todo el código
COPY . .

EXPOSE 8000

# Ejecutamos uvicorn directamente
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]