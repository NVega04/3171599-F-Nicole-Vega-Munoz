"""
Task Manager API - Simulación de Base de Datos
Semana 04 - Proyecto

Base de datos en memoria para el proyecto.
"""

"""
QUE:    Simula una base de datos en memoria (in-memory) para almacenar los servicios de traducción durante el desarrollo y pruebas. Incluye inicialización con datos de ejemplo.
PARA:   Permitir pruebas rápidas sin necesidad de PostgreSQL/MySQL/etc., mantener el estado de los servicios entre peticiones (mientras el servidor está corriendo), y proporcionar datos iniciales para demostrar la funcionalidad de la API en /docs.
IMPACTO: Si está bien implementado → desarrollo ágil, pruebas fáciles, datos de ejemplo coherentes con el dominio y buena demostración en Swagger / Si no se adapta o tiene errores → datos inconsistentes, endpoints que fallan por falta de datos, o confusión en la evaluación al no reflejar el dominio real.
"""

from datetime import datetime, timezone

from models import ServiceStatus, ServiceType


# Simulated database (in-memory)
services_db: dict[int, dict] = {}
service_id_counter: int = 0


def get_next_id() -> int:
    """Genera el siguiente ID para un servicio"""
    global service_id_counter
    service_id_counter += 1
    return service_id_counter


def seed_database() -> None:
    """Inicializa la base de datos con servicios de traducción de ejemplo"""
    global services_db, service_id_counter

    sample_services = [
        {
            "document_title": "Contrato de arrendamiento",
            "client_name": "María García López",
            "source_language": "español",
            "target_language": "inglés",
            "service_type": ServiceType.LEGAL,
            "word_count": 2500,
            "price": 350000.0,
            "deadline_days": 5,
            "notes": "Requiere terminología jurídica especializada",
            "status": ServiceStatus.AVAILABLE,
        },
        {
            "document_title": "Manual técnico de software",
            "client_name": "TechCorp S.A.S.",
            "source_language": "inglés",
            "target_language": "español",
            "service_type": ServiceType.TECHNICAL,
            "word_count": 8000,
            "price": 720000.0,
            "deadline_days": 10,
            "notes": "Incluye glosario de términos técnicos",
            "status": ServiceStatus.RESERVED,
        },
        {
            "document_title": "Certificado de nacimiento",
            "client_name": "Carlos Martínez Ruiz",
            "source_language": "español",
            "target_language": "francés",
            "service_type": ServiceType.CERTIFIED,
            "word_count": 300,
            "price": 85000.0,
            "deadline_days": 2,
            "notes": "Traducción jurada con sello y firma",
            "status": ServiceStatus.AVAILABLE,
        },
        {
            "document_title": "Correspondencia comercial",
            "client_name": "Exportaciones del Valle",
            "source_language": "español",
            "target_language": "alemán",
            "service_type": ServiceType.EXPRESS,
            "word_count": 1200,
            "price": 180000.0,
            "deadline_days": 1,
            "notes": "Urgente - necesita entrega en 24 horas",
            "status": ServiceStatus.COMPLETED,
        },
    ]

    for service_data in sample_services:
        service_id = get_next_id()
        now = datetime.now(timezone.utc)

        services_db[service_id] = {
            "id": service_id,
            "document_title": service_data["document_title"],
            "client_name": service_data["client_name"],
            "source_language": service_data["source_language"],
            "target_language": service_data["target_language"],
            "service_type": service_data["service_type"],
            "word_count": service_data.get("word_count"),
            "price": service_data["price"],
            "deadline_days": service_data.get("deadline_days"),
            "notes": service_data.get("notes"),
            "status": service_data["status"],
            "created_at": now,
            "updated_at": None,
            "reserved_at": now
            if service_data["status"] == ServiceStatus.RESERVED
            else None,
            "completed_at": now
            if service_data["status"] == ServiceStatus.COMPLETED
            else None,
        }


# Inicializar con datos de ejemplo
seed_database()
