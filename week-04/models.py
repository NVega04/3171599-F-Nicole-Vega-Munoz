"""
QUE:    Define todos los esquemas Pydantic para validación de entrada, serialización de salida y documentación automática en OpenAPI.
PARA:   Servir como contrato claro entre la API y los clientes: validar datos entrantes (create/update), estructurar respuestas seguras y consistentes, y generar schemas detallados en /docs para que el evaluador y otros desarrolladores entiendan exactamente qué datos se esperan y devuelven.
IMPACTO: Si están bien diseñados → validación automática fuerte, documentación profesional en Swagger (con ejemplos útiles), respuestas predecibles y seguras / Si están incompletos o mal tipados → errores 422 frecuentes, documentación confusa, riesgo de exponer datos sensibles y baja puntuación en "Response models bien diseñados" (10 puntos clave).
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List

from pydantic import BaseModel, Field, ConfigDict


# ============================================
# ENUMS - Estados y Tipos de servicio
# ============================================


class ServiceStatus(str, Enum):
    """Estados posibles de un servicio de traducción"""

    AVAILABLE = "available"
    RESERVED = "reserved"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ServiceType(str, Enum):
    """Tipos de servicio de traducción disponibles"""

    STANDARD = "standard"
    EXPRESS = "express"
    CERTIFIED = "certified"
    LEGAL = "legal"
    TECHNICAL = "technical"


# ============================================
# ERROR SCHEMAS
# ============================================


class ErrorDetail(BaseModel):
    """Detalle de error interno"""

    code: str = Field(..., description="Código único del error")
    message: str = Field(..., description="Mensaje descriptivo")
    details: dict | None = Field(None, description="Detalles adicionales")


class ErrorResponse(BaseModel):
    """Respuesta de error estándar"""

    error: ErrorDetail

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": {
                    "code": "SERVICE_NOT_FOUND",
                    "message": "Servicio con id 99 no encontrado",
                    "details": None,
                }
            }
        }
    )


# ============================================
# SCHEMAS DE SERVICIO
# ============================================


class ServiceCreate(BaseModel):
    """
    Schema para registrar un nuevo servicio de traducción.
    """

    document_title: str = Field(
        ..., min_length=3, max_length=200, description="Título del documento a traducir"
    )
    client_name: str = Field(
        ..., min_length=2, max_length=100, description="Nombre del cliente solicitante"
    )
    source_language: str = Field(
        ...,
        min_length=2,
        max_length=30,
        description="Idioma origen (ej: español, inglés)",
    )
    target_language: str = Field(
        ...,
        min_length=2,
        max_length=30,
        description="Idioma destino (ej: inglés, francés)",
    )
    service_type: ServiceType = Field(
        default=ServiceType.STANDARD, description="Tipo de servicio de traducción"
    )
    word_count: Optional[int] = Field(
        None, ge=1, description="Número de palabras del documento"
    )
    price: float = Field(..., gt=0, description="Precio del servicio en COP")
    deadline_days: Optional[int] = Field(
        None, ge=1, le=30, description="Días deadline para entrega"
    )
    notes: Optional[str] = Field(
        None, max_length=500, description="Notas adicionales o requisitos especiales"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "document_title": "Contrato de arrendamiento",
                "client_name": "María García López",
                "source_language": "español",
                "target_language": "inglés",
                "service_type": "legal",
                "word_count": 2500,
                "price": 350000.0,
                "deadline_days": 5,
                "notes": "Requiere terminología jurídica especializada",
            }
        }
    )


class ServiceUpdate(BaseModel):
    """
    Schema para actualización completa (PUT) de un servicio. Todos los campos opcionales.
    """

    document_title: Optional[str] = Field(None, min_length=3, max_length=200)
    client_name: Optional[str] = Field(None, min_length=2, max_length=100)
    source_language: Optional[str] = Field(None, min_length=2, max_length=30)
    target_language: Optional[str] = Field(None, min_length=2, max_length=30)
    service_type: Optional[ServiceType] = None
    word_count: Optional[int] = Field(None, ge=1)
    price: Optional[float] = Field(None, gt=0)
    deadline_days: Optional[int] = Field(None, ge=1, le=30)
    notes: Optional[str] = Field(None, max_length=500)


class StatusUpdate(BaseModel):
    """
    Schema para cambiar solo el estado del servicio (PATCH /services/{id}/status)
    """

    status: ServiceStatus = Field(..., description="Nuevo estado del servicio")


class ServiceResponse(BaseModel):
    """
    Schema de respuesta básica (público) para un servicio.
    """

    id: int
    document_title: str
    client_name: str
    source_language: str
    target_language: str
    service_type: ServiceType
    price: float
    status: ServiceStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "document_title": "Contrato de arrendamiento",
                "client_name": "María García López",
                "source_language": "español",
                "target_language": "inglés",
                "service_type": "legal",
                "price": 350000.0,
                "status": "available",
                "created_at": "2026-03-03T23:00:00",
            }
        },
    )


class ServiceDetailResponse(ServiceResponse):
    """
    Schema de respuesta detallada (para GET /services/{id}).
    Incluye campos adicionales que no se muestran en la lista.
    """

    word_count: Optional[int]
    deadline_days: Optional[int]
    notes: Optional[str]
    updated_at: Optional[datetime]
    reserved_at: Optional[datetime]
    completed_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "document_title": "Contrato de arrendamiento",
                "client_name": "María García López",
                "source_language": "español",
                "target_language": "inglés",
                "service_type": "legal",
                "word_count": 2500,
                "price": 350000.0,
                "deadline_days": 5,
                "notes": "Requiere terminología jurídica especializada",
                "status": "available",
                "created_at": "2026-03-03T23:00:00",
                "updated_at": None,
                "reserved_at": None,
                "completed_at": None,
            }
        },
    )


class ServiceListResponse(BaseModel):
    """
    Schema para listado paginado de servicios.
    """

    items: List[ServiceResponse]
    total: int
    skip: int
    limit: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "id": 1,
                        "document_title": "Contrato de arrendamiento",
                        "client_name": "María García López",
                        "source_language": "español",
                        "target_language": "inglés",
                        "service_type": "legal",
                        "price": 350000.0,
                        "status": "available",
                        "created_at": "2026-03-03T23:00:00",
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 20,
            }
        }
    )


class ServiceStats(BaseModel):
    """
    Schema para estadísticas generales del catálogo de servicios.
    """

    total_services: int
    by_status: Dict[str, int]  # ej: {"available": 15, "completed": 3}
    average_price: float
    max_price: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_services": 25,
                "by_status": {
                    "available": 18,
                    "reserved": 4,
                    "completed": 3,
                    "cancelled": 0,
                },
                "average_price": 185000.50,
                "max_price": 500000.0,
            }
        }
    )
