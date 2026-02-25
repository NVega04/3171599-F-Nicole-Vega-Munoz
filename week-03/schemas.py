"""
Schemas Pydantic - Gestión de Traducciones
==========================================

Modelos de validación de datos para servicios y especialidades.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List, Optional


# ============================================
# ENUMS (Criterios de ordenamiento)
# ============================================

class SortOrder(str, Enum):
    """Dirección del ordenamiento"""
    asc = "asc"
    desc = "desc"


class ProductSortField(str, Enum):
    """Campos permitidos para ordenar los servicios"""
    name = "name"
    price = "price"
    created_at = "created_at"
    stock = "stock"


# ============================================
# CATEGORY SCHEMAS (Especialidades)
# ============================================

class CategoryBase(BaseModel):
    """Atributos básicos de una especialidad de traducción"""
    name: str = Field(..., min_length=2, max_length=50, example="Traducción Jurada")
    description: str | None = Field(default=None, max_length=200, example="Documentos con validez legal")


class CategoryCreate(CategoryBase):
    """Modelo para registrar una nueva especialidad"""
    pass


class CategoryUpdate(BaseModel):
    """Modelo para modificar una especialidad (campos opcionales)"""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=200)


class CategoryResponse(CategoryBase):
    """Estructura de salida para una especialidad"""
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ============================================
# PRODUCT SCHEMAS (Servicios)
# ============================================

class ProductBase(BaseModel):
    """Atributos básicos de un servicio de traducción"""
    name: str = Field(..., min_length=2, max_length=100, example="Traducción ES-EN")
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(..., gt=0, description="Tarifa por palabra o unidad de medida")
    stock: int = Field(default=0, ge=0, description="Cantidad de traductores/recursos disponibles")
    tags: List[str] = Field(default=[], example=["#urgente", "#nativo"])


class ProductCreate(ProductBase):
    """Modelo para dar de alta un nuevo servicio"""
    category_id: int = Field(..., gt=0, description="ID de la especialidad asociada")


class ProductUpdate(BaseModel):
    """Modelo para actualización parcial de un servicio"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    category_id: Optional[int] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    tags: Optional[List[str]] = None


class ProductResponse(ProductBase):
    """Estructura de salida completa para un servicio"""
    id: int
    category_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    # Incluye el objeto completo de la categoría si está disponible
    category: Optional[CategoryResponse] = None

    model_config = {"from_attributes": True}


# ============================================
# PAGINATION SCHEMAS
# ============================================

class PaginatedResponse(BaseModel):
    """Modelo estándar para respuestas con múltiples resultados"""
    items: List[ProductResponse]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool