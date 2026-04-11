# Translation Services API - Semana 04

API REST desarrollada con **FastAPI** para la gestión de **servicios de traducción profesionales**. Proyecto correspondiente a la Semana 04 del bootcamp.

## Descripción

Esta API permite:
- Registrar servicios de traducción profesional
- Listar y filtrar servicios por estado, tipo, idiomas y precio máximo
- Gestionar el estado de los servicios (available → reserved → completed / cancelled)
- Obtener estadísticas básicas del catálogo de servicios
- Manejo consistente de errores con códigos y mensajes personalizados

Todo el proyecto está adaptado al dominio de **servicios de traducción profesionales**, con estados y transiciones de negocio coherentes.

## Tecnologías utilizadas

- **Framework**: FastAPI
- **Validación y serialización**: Pydantic
- **Gestión de dependencias**: uv
- **Base de datos**: In-memory (simulada con diccionario)
- **Contenerización**: Docker + Docker Compose
- **Documentación automática**: OpenAPI / Swagger UI

## Instalación y ejecución local

### Requisitos

- Python 3.12+
- uv (recomendado)
- Docker + Docker Compose (opcional)

### Pasos

1. Clonar el repositorio

```bash
git clone <tu-repo-url>
cd <nombre-carpeta>
```

2. Crear y activar entorno virtual

```bash
uv venv
source .venv/bin/activate   # Linux/Mac
# o en Windows: .venv\Scripts\activate
```

3. Instalar dependencias

```bash
uv sync
```

4. Ejecutar la API (modo desarrollo)

```bash
uv run fastapi dev main.py --reload
```

### Accede a:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Con Docker

```bash
docker compose up --build
```

Accede a http://localhost:8000/docs (o el puerto configurado en docker-compose.yml)

# Endpoints principales

|Método|Ruta  |Descripción                              |
|------|------|-----------------------------------------|
GET    |/services |Listar servicios (con filtros y paginación)
GET|/services/{service_id}|Obtener detalle de un servicio|
POST|/services|Registrar nuevo servicio de traducción|
PUT|/services/{service_id}|Actualizar completamente un servicio|
PATCH|/services/{service_id}/status|Cambiar estado del servicio|
GET|/services/stats|Estadísticas del catálogo|
GET|/health|Health check del servicio|

# Estados del servicio y transiciones válidas

```text
available ──► reserved ──► completed
   │             │
   └─────────────┴───────► cancelled
```

Transiciones permitidas:

- available → reserved / cancelled
- reserved → completed / cancelled
- No se permiten retrocesos (completed/cancelled no vuelven a estados anteriores)

# Tipos de servicio

- **standard**: Traducción estándar (3-5 días)
- **express**: Traducción urgente (24-48 horas)
- **certified**: Traducción jurada certificada
- **legal**: Documentos legales especializados
- **technical**: Manuales y documentación técnica