"""
Dependencias Reutilizables
==========================

Define dependencias para paginación, filtros y ordenamiento.

TODO: Completa las dependencias siguiendo las instrucciones.
"""

from fastapi import Query, Depends
from typing import Annotated
from schemas import SortOrder, ProductSortField


# ============================================
# PAGINACIÓN
# ============================================

class PaginationParams:
    """
    Controla el desplazamiento y límite de resultados en la lista de servicios.
    """
    
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Número de página (mínimo 1)"),
        per_page: int = Query(default=10, ge=1, le=50, description="Servicios por página (máximo 50)")
    ):
        self.page = page
        self.per_page = per_page
        self.offset = (page - 1) * per_page


# Alias para inyección de dependencias
PaginationDep = Annotated[PaginationParams, Depends()]

# ============================================
# FILTROS DE PRODUCTOS
# ============================================

class ProductFilters:
    """
    Parámetros para refinar la búsqueda de servicios de traducción.
    """
    
    def __init__(
        self,
        search: str | None = Query(
            default=None, 
            min_length=2, 
            description="Buscar texto en el nombre o descripción del servicio"
        ),
        category_id: int | None = Query(
            default=None, 
            gt=0, 
            description="Filtrar por el ID de la especialidad (Legal, Técnica, etc.)"
        ),
        min_price: float | None = Query(
            default=None, 
            ge=0, 
            description="Precio mínimo por palabra o proyecto"
        ),
        max_price: float | None = Query(
            default=None, 
            ge=0, 
            description="Precio máximo por palabra o proyecto"
        ),
        in_stock: bool | None = Query(
            default=None, 
            description="¿Hay traductores disponibles actualmente para este servicio?"
        ),
        tags: list[str] = Query(
            default=[], 
            description="Lista de etiquetas para filtrar (ej. #urgente, #nativo)"
        )
    ):
        self.search = search
        self.category_id = category_id
        self.min_price = min_price
        self.max_price = max_price
        self.in_stock = in_stock
        self.tags = tags


# Alias para inyección de dependencias
ProductFiltersDep = Annotated[ProductFilters, Depends()]


# ============================================
# ORDENAMIENTO
# ============================================

class SortingParams:
    """
    Define el criterio y la dirección de ordenamiento de los resultados.
    """
    
    def __init__(
        self,
        sort_by: ProductSortField = Query(
            default=ProductSortField.name, 
            description="Campo por el cual ordenar los servicios"
        ),
        order: SortOrder = Query(
            default=SortOrder.asc, 
            description="Dirección del orden: ascendente (asc) o descendente (desc)"
        )
    ):
        self.sort_by = sort_by
        self.order = order


# Alias para inyección de dependencias
SortingDep = Annotated[SortingParams, Depends()]