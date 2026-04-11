"""
QUE:    Punto de entrada principal de la API FastAPI. Define la aplicación, configura metadata (título, descripción, tags, etc.), registra handlers de excepciones, funciones helper y todos los endpoints de la API.
PARA:   Servir como el núcleo central que une todos los componentes del proyecto (modelos, base de datos in-memory, excepciones, rutas). Es el archivo que FastAPI ejecuta primero y el que genera la documentación automática en /docs.
IMPACTO: Si está bien estructurado y documentado → excelente experiencia de desarrollo y documentación clara / Si tiene errores o falta metadata → documentación pobre, endpoints confusos, manejo de errores inconsistente y dificultad para depurar.
"""

from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import FastAPI, Path, Query, status

from models import (
    ServiceStatus,
    ServiceType,
    ServiceCreate,
    ServiceUpdate,
    StatusUpdate,
    ServiceResponse,
    ServiceListResponse,
    ServiceStats,
    ErrorResponse,
)
from database import services_db, get_next_id
from exceptions import (
    ServiceException,
    ServiceNotFoundError,
    InvalidStatusTransitionError,
    DuplicateServiceError,
    service_exception_handler,
)


# ============================================
# CONFIGURACIÓN DE LA APP
# ============================================

tags_metadata = [
    {
        "name": "services",
        "description": "Operaciones CRUD sobre servicios de traducción",
    },
    {
        "name": "stats",
        "description": "Estadísticas generales del catálogo de servicios",
    },
    {"name": "health", "description": "Verificación del estado del servicio"},
]

app = FastAPI(
    title="Professional Translation Services API",
    description="""
    API REST para la gestión de **servicios de traducción profesionales**.

    Funcionalidades principales:
    - Registrar servicios de traducción
    - Buscar y filtrar servicios por estado, tipo, idioma origen/destino y precio
    - Gestionar el estado del servicio (available → reserved → completed)
    - Estadísticas básicas del catálogo
    """,
    version="1.0.0",
    contact={
        "name": "Yohan - Bootcamp FastAPI",
        "url": "https://github.com/tu-usuario",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ============================================
# MANEJADORES DE EXCEPCIONES
# ============================================

app.add_exception_handler(ServiceException, service_exception_handler)


# ============================================
# FUNCIONES HELPER
# ============================================


def validate_status_transition(current: ServiceStatus, target: ServiceStatus) -> bool:
    """
    Reglas de transición de estado para servicios de traducción:
    - available   → reserved    OK
    - available   → cancelled  OK
    - reserved    → completed  OK
    - reserved    → cancelled  OK
    - completed   → cualquier  NO
    - cancelled   → cualquier  NO
    """
    allowed = {
        ServiceStatus.AVAILABLE: [ServiceStatus.RESERVED, ServiceStatus.CANCELLED],
        ServiceStatus.RESERVED: [ServiceStatus.COMPLETED, ServiceStatus.CANCELLED],
        ServiceStatus.COMPLETED: [],
        ServiceStatus.CANCELLED: [],
    }
    return target in allowed.get(current, [])


def check_duplicate_service(
    document_title: str,
    source_lang: str,
    target_lang: str,
    exclude_id: int | None = None,
) -> bool:
    """Verifica si ya existe un servicio con el mismo documento e idiomas"""
    for service_id, service in services_db.items():
        if (
            service["document_title"].lower() == document_title.lower()
            and service["source_language"].lower() == source_lang.lower()
            and service["target_language"].lower() == target_lang.lower()
        ):
            if exclude_id is None or service_id != exclude_id:
                return True
    return False


# ============================================
# ENDPOINTS
# ============================================


@app.get(
    "/services",
    response_model=ServiceListResponse,
    tags=["services"],
    summary="Listar servicios de traducción",
    description="Devuelve una lista paginada de servicios con filtros opcionales por estado, tipo, idiomas y precio máximo",
    responses={
        200: {"model": ServiceListResponse},
        422: {"model": ErrorResponse},
    },
)
async def list_services(
    status: Annotated[
        ServiceStatus | None, Query(description="Filtrar por estado del servicio")
    ] = None,
    service_type: Annotated[
        ServiceType | None, Query(description="Filtrar por tipo de servicio")
    ] = None,
    source_language: Annotated[
        str | None, Query(description="Filtrar por idioma origen")
    ] = None,
    target_language: Annotated[
        str | None, Query(description="Filtrar por idioma destino")
    ] = None,
    max_price: Annotated[
        float | None, Query(gt=0, description="Precio máximo en COP")
    ] = None,
    skip: Annotated[int, Query(ge=0, description="Offset para paginación")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Límite de resultados")] = 20,
):
    filtered = list(services_db.values())

    if status:
        filtered = [s for s in filtered if s["status"] == status]
    if service_type:
        filtered = [s for s in filtered if s["service_type"] == service_type]
    if source_language:
        filtered = [
            s
            for s in filtered
            if s["source_language"].lower() == source_language.lower()
        ]
    if target_language:
        filtered = [
            s
            for s in filtered
            if s["target_language"].lower() == target_language.lower()
        ]
    if max_price:
        filtered = [s for s in filtered if s["price"] <= max_price]

    total = len(filtered)
    paginated = filtered[skip : skip + limit]

    return ServiceListResponse(
        items=[ServiceResponse(**s) for s in paginated],
        total=total,
        skip=skip,
        limit=limit,
    )


@app.get(
    "/services/{service_id}",
    response_model=ServiceResponse,
    tags=["services"],
    summary="Obtener detalle de un servicio específico",
    responses={
        200: {"model": ServiceResponse},
        404: {"model": ErrorResponse},
    },
)
async def get_service(
    service_id: Annotated[int, Path(ge=1, description="ID del servicio")],
):
    if service_id not in services_db:
        raise ServiceNotFoundError(service_id)

    return ServiceResponse(**services_db[service_id])


@app.post(
    "/services",
    status_code=status.HTTP_201_CREATED,
    response_model=ServiceResponse,
    tags=["services"],
    summary="Registrar un nuevo servicio de traducción",
    responses={
        201: {"model": ServiceResponse},
        409: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
async def create_service(service: ServiceCreate):
    if check_duplicate_service(
        service.document_title, service.source_language, service.target_language
    ):
        raise DuplicateServiceError(
            service.document_title, service.source_language, service.target_language
        )

    now = datetime.now(timezone.utc)
    new_id = get_next_id()

    data = service.model_dump()
    data.update(
        {
            "id": new_id,
            "status": ServiceStatus.AVAILABLE,
            "created_at": now,
            "updated_at": now,
            "reserved_at": None,
            "completed_at": None,
        }
    )

    services_db[new_id] = data
    return ServiceResponse(**data)


@app.patch(
    "/services/{service_id}/status",
    response_model=ServiceResponse,
    tags=["services"],
    summary="Actualizar el estado de un servicio",
    description="Permite cambiar el estado siguiendo reglas de negocio (available → reserved → completed, etc.)",
    responses={
        200: {"model": ServiceResponse},
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def update_service_status(
    service_id: Annotated[int, Path(ge=1, description="ID del servicio")],
    status_update: StatusUpdate,
):
    if service_id not in services_db:
        raise ServiceNotFoundError(service_id)

    current = services_db[service_id]
    current_status = current["status"]
    new_status = status_update.status

    if not validate_status_transition(current_status, new_status):
        raise InvalidStatusTransitionError(current_status, new_status)

    now = datetime.now(timezone.utc)
    update_data = {"status": new_status, "updated_at": now}

    if new_status == ServiceStatus.RESERVED:
        update_data["reserved_at"] = now
    elif new_status == ServiceStatus.COMPLETED:
        update_data["completed_at"] = now

    current.update(update_data)
    services_db[service_id] = current

    return ServiceResponse(**current)


@app.get(
    "/services/stats",
    response_model=ServiceStats,
    tags=["stats"],
    summary="Obtener estadísticas generales del catálogo de servicios",
    responses={200: {"model": ServiceStats}},
)
async def get_stats():
    if not services_db:
        return ServiceStats(
            total_services=0, by_status={}, average_price=0.0, max_price=0.0
        )

    total = len(services_db)
    by_status = {}
    prices = []

    for service in services_db.values():
        st = service["status"]
        by_status[st.value] = by_status.get(st.value, 0) + 1
        prices.append(service["price"])

    avg_price = sum(prices) / total if prices else 0
    max_p = max(prices) if prices else 0

    return ServiceStats(
        total_services=total,
        by_status=by_status,
        average_price=round(avg_price, 2),
        max_price=max_p,
    )


# ============================================
# HEALTH CHECK
# ============================================


@app.get(
    "/health",
    tags=["health"],
    summary="Health check del servicio",
    response_description="Confirma que la API está operativa",
)
async def health_check():
    """Endpoint simple para verificar que el servicio está corriendo correctamente."""
    return {
        "status": "healthy",
        "service": "translation-services-api",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
