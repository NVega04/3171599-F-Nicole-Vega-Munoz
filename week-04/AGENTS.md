# AGENTS.md

## Project: Professional Translation Services API

FastAPI REST API for managing professional translation services with status transitions.

## Commands

```bash
# Install dependencies
uv sync

# Run dev server (recommended)
uv run fastapi dev main.py --reload

# Or with uvicorn directly
uv run uvicorn main:app --reload

# Run tests (pytest installed as dev dependency)
uv run pytest

# Docker
docker compose up --build
```

## Architecture

- **Entry point**: `main.py` - FastAPI app, endpoints, business logic
- **Models**: `models.py` - Pydantic schemas, enums (ServiceStatus, ServiceType)
- **Database**: `database.py` - In-memory dict (`services_db`), auto-seeded on import
- **Exceptions**: `exceptions.py` - Custom exceptions with handler registered in main.py

## Key Conventions

- API docs at `/docs` (Swagger) and `/redoc`
- Status transitions: `available → reserved → completed` or `available/reserved → cancelled`
- Error responses follow `{ "error": { "code", "message", "details" } }` format
- Duplicate services (same document_title + source_language + target_language) rejected with 409

## Quirks

- Database is in-memory; data resets on server restart
- Sample data seeded automatically from `database.py:seed_database()`
- pyproject.toml project name is "task-manager-api" but this is a translation services API
- Dockerfile uses Python 3.13, pyproject.toml requires >=3.14 (version mismatch)
