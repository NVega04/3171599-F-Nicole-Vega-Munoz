"""
Base de Datos Simulada
======================

Datos en memoria para el proyecto.
"""

from datetime import datetime

# ============================================
# CATEGORÍAS
# ============================================

categories_db: dict[int, dict] = {
    1: {
        "id": 1,
        "name": "Traducción Jurada",
        "description": "Traducciones oficiales con validez legal ante organismos públicos.",
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
    2: {
        "id": 2,
        "name": "Traducción Técnica",
        "description": "Documentación de ingeniería, manuales y textos científicos.",
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
    3: {
        "id": 3,
        "name": "Localización de Software",
        "description": "Adaptación de apps, videojuegos y sitios web al mercado local.",
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
    4: {
        "id": 4,
        "name": "Traducción Audiovisual",
        "description": "Subtitulado, doblaje y transcripción de contenido multimedia.",
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
}

next_category_id = 5

# ============================================
# PRODUCTOS
# ============================================

products_db: dict[int, dict] = {
    1: {
        "id": 1,
        "name": "Traducción Jurada ES-EN (Certificado Nacimiento)",
        "description": "Traducción oficial de español a inglés para trámites migratorios.",
        "price": 0.12,  # Tarifa por palabra
        "category_id": 1,
        "stock": 10,    # Disponibilidad de traductores en turno
        "tags": ["oficial", "urgente", "legal"],
        "created_at": datetime(2024, 1, 15, 9, 0, 0)
    },
    2: {
        "id": 2,
        "name": "Manual Técnico de Maquinaria Pesada",
        "description": "Traducción técnica EN-ES de manuales de operación industrial.",
        "price": 0.08,
        "category_id": 2,
        "stock": 5,
        "tags": ["ingenieria", "especializado"],
        "created_at": datetime(2024, 2, 1, 10, 0, 0)
    },
    3: {
        "id": 3,
        "name": "Localización de App Móvil (iOS/Android)",
        "description": "Adaptación cultural y lingüística de interfaces de usuario.",
        "price": 0.15,
        "category_id": 3,
        "stock": 8,
        "tags": ["tech", "ux", "popular"],
        "created_at": datetime(2024, 1, 20, 14, 0, 0)
    },
    4: {
        "id": 4,
        "name": "Subtitulado de Serie Documental",
        "description": "Creación y sincronización de subtítulos para plataformas de streaming.",
        "price": 5.50,  # Tarifa por minuto de video
        "category_id": 4,
        "stock": 3,
        "tags": ["multimedia", "netflix-ready"],
        "created_at": datetime(2024, 3, 1, 8, 0, 0)
    },
    5: {
        "id": 5,
        "name": "Traducción de Contratos Mercantiles",
        "description": "Traducción legal de contratos de confidencialidad y términos de servicio.",
        "price": 0.10,
        "category_id": 1,
        "stock": 12,
        "tags": ["corporativo", "legal"],
        "created_at": datetime(2024, 2, 15, 11, 0, 0)
    },
    6: {
        "id": 6,
        "name": "Localización de E-commerce (Shopify)",
        "description": "Traducción de catálogos de productos y pasarelas de pago.",
        "price": 0.07,
        "category_id": 3,
        "stock": 20,
        "tags": ["ventas", "web"],
        "created_at": datetime(2024, 2, 20, 16, 0, 0)
    },
    7: {
        "id": 7,
        "name": "Traducción Médica (Protocolos Clínicos)",
        "description": "Traducción altamente especializada de estudios médicos y farmacológicos.",
        "price": 0.18,
        "category_id": 2,
        "stock": 0,  # Sin traductores disponibles actualmente
        "tags": ["medicina", "premium"],
        "created_at": datetime(2024, 3, 5, 9, 0, 0)
    },
    8: {
        "id": 8,
        "name": "Transcripción de Conferencias Académicas",
        "description": "Paso de audio a texto de ponencias universitarias con limpieza de muletillas.",
        "price": 3.00, # Tarifa por minuto de audio
        "category_id": 4,
        "stock": 15,
        "tags": ["academico", "audio"],
        "created_at": datetime(2024, 3, 10, 10, 0, 0)
    },
}

next_product_id = 9


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_next_category_id() -> int:
    """
    Obtener el siguiente identificador único para una categoría e incrementar el contador global.
    Este ID se asigna automáticamente al registrar una nueva especialidad de traducción.
    """
    global next_category_id
    current = next_category_id
    next_category_id += 1
    return current


def get_next_product_id() -> int:
    """
    Obtener el siguiente identificador único para un servicio e incrementar el contador global.
    Asegura que cada servicio de traducción (producto) tenga una referencia única en el sistema.
    """
    global next_product_id
    current = next_product_id
    next_product_id += 1
    return current