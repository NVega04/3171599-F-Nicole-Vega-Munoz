"""
Router de Productos
===================

CRUD con filtrado, paginación y ordenamiento.

TODO: Implementa los endpoints siguiendo las instrucciones.
"""

from fastapi import APIRouter, Path, HTTPException, status
from datetime import datetime

from database import products_db, categories_db, get_next_product_id
from schemas import ProductCreate, ProductUpdate, ProductResponse, SortOrder
from dependencies import PaginationDep, ProductFiltersDep, SortingDep

router = APIRouter(
    prefix="/products",
    tags=["Servicios de Traducción"],
    responses={404: {"description": "Servicio no encontrado"}}
)


# ============================================
# GET /products - Listar con filtros
# ============================================

@router.get("/", response_model=dict)
async def list_products(
    pagination: PaginationDep,
    filters: ProductFiltersDep,
    sorting: SortingDep
):
    """
    Lista todos los servicios de traducción profesional disponibles.
    
    Permite aplicar filtros por:
    - Búsqueda textual: En nombre y descripción del servicio.
    - Categoría: Filtrar por especialidad (Legal, Médica, etc.).
    - Rango de precios: Costo por palabra o por proyecto.
    - Disponibilidad: Servicios activos en el catálogo.
    - Etiquetas: Filtrar por tags como #urgente, #nativo o #tecnico.
    """
    
    # 1. Obtener todos los servicios registrados en la base de datos
    all_services = list(products_db.values())
    filtered_services = all_services

    # 2. Aplicar filtros de búsqueda y negocio
    # Filtrado por coincidencia de texto (nombre o descripción)
    if filters.search:
        search_query = filters.search.lower()
        filtered_services = [
            item for item in filtered_services 
            if search_query in item["name"].lower() or search_query in item["description"].lower()
        ]

    # Filtrado por ID de categoría (especialidad de traducción)
    if filters.category_id:
        filtered_services = [item for item in filtered_services if item["category_id"] == filters.category_id]

    # Filtrado por rango de precios (mínimo y máximo)
    if filters.min_price is not None:
        filtered_services = [item for item in filtered_services if item["price"] >= filters.min_price]
    
    if filters.max_price is not None:
        filtered_services = [item for item in filtered_services if item["price"] <= filters.max_price]

    # Filtrado por disponibilidad (Stock > 0 indica que hay traductores disponibles)
    if filters.in_stock is not None:
        filtered_services = [item for item in filtered_services if (item["stock"] > 0) == filters.in_stock]

    # Filtrado por etiquetas (Verifica si el servicio tiene al menos una de las etiquetas buscadas)
    if filters.tags:
        filtered_services = [
            item for item in filtered_services 
            if any(tag in item.get("tags", []) for tag in filters.tags)
        ]

    # 3. Aplicar ordenamiento según los parámetros de la solicitud
    is_descending = sorting.order == SortOrder.DESC
    filtered_services.sort(key=lambda x: x.get(sorting.sort_by, "id"), reverse=is_descending)

    # 4. Lógica de paginación
    total_records = len(filtered_services)
    start_index = (pagination.page - 1) * pagination.per_page
    end_index = start_index + pagination.per_page
    
    paginated_items = filtered_services[start_index:end_index]
    total_pages_count = math.ceil(total_records / pagination.per_page)

    # 5. Retornar los resultados con metadatos de navegación
    return {
        "items": paginated_items,
        "total": total_records,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": total_pages_count,
        "has_next": pagination.page < total_pages_count,
        "has_prev": pagination.page > 1
    }

# ============================================
# GET /products/{id} - Obtener uno
# ============================================

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int = Path(..., gt=0, title="ID del Servicio", description="Identificador numérico del servicio de traducción")
):
    """
    Obtiene la información detallada de un servicio de traducción específico.
    
    El resultado incluye los datos básicos del servicio y la información 
    expandida de la categoría (especialidad) a la que pertenece.
    """
    
    # 1. Buscar el servicio en la base de datos por su ID
    service_entry = products_db.get(product_id)
    
    # 2. Validar existencia (Si no existe, lanzar error 404 con mensaje en español)
    if not service_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lo sentimos, el servicio con ID {product_id} no existe en nuestro catálogo de traducción."
        )
    
    # 3. Enriquecer la respuesta con los datos de la categoría
    category_id = service_entry.get("category_id")
    category_data = categories_db.get(category_id)
    
    # Creamos una copia del objeto para añadirle la información de la categoría
    detailed_response = service_entry.copy()
    detailed_response["category"] = category_data if category_data else "Sin categoría asignada"

    # 4. Retornar el servicio completo
    return detailed_response

# ============================================
# POST /products - Crear nuevo servicio
# ============================================

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_product(product_data: ProductCreate):
    """
    Registra un nuevo servicio de traducción en el catálogo.
    
    Proceso:
    1. Valida que la categoría (especialidad) exista.
    2. Asigna un identificador único automáticamente.
    3. Almacena los detalles técnicos y comerciales.
    4. Retorna el registro completo del servicio creado.
    """
    
    # 1. Verificar que category_id existe (Validación de integridad técnica)
    # Si la especialidad (médica, legal, etc.) no existe, no podemos crear el servicio.
    if product_data.category_id not in categories_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: La categoría con ID {product_data.category_id} no existe. "
                   "Debe asignar una especialidad válida para crear el servicio."
        )

    # 2. Obtener nuevo ID (Lógica de base de datos)
    new_service_id = get_next_product_id()
    
    # 3. Crear diccionario con los datos (Technical data structure)
    # Combinamos el nuevo ID, los datos del esquema y la fecha de registro
    new_service_record = {
        "id": new_service_id,
        **product_data.dict(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    # 4. Guardar en products_db
    products_db[new_service_id] = new_service_record
    
    # 5. Enriquecer la respuesta para el usuario
    # Incluimos los datos de la categoría para que la confirmación sea completa
    response_data = new_service_record.copy()
    response_data["category"] = categories_db.get(product_data.category_id)

    # Retornar el producto creado con su información expandida
    return response_data


# ============================================
# PUT /products/{id} - Actualizar completo
# ============================================

@router.put("/{product_id}", response_model=ProductResponse)
async def replace_product(
    product_id: int = Path(..., gt=0, title="ID del Servicio", description="ID del servicio que se desea reemplazar"),
    product_update: ProductCreate = ...
):
    """
    Reemplaza la información de un servicio de traducción existente de forma integral.
    
    Proceso de actualización:
    1. Verifica la existencia del servicio original.
    2. Valida que la nueva categoría asignada sea válida.
    3. Sustituye todos los valores previos por los nuevos datos proporcionados.
    4. Registra la fecha de la última modificación.
    """
    
    # 1. Verificar que el producto existe (404 si no se encuentra)
    if product_id not in products_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede actualizar: El servicio con ID {product_id} no existe."
        )

    # 2. Verificar que la categoría (category_id) existe (400 si es inválida)
    if product_update.category_id not in categories_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Categoría inválida: La categoría {product_update.category_id} no está registrada."
        )

    # 3. Reemplazar todos los campos (Full replacement logic)
    # Recuperamos la fecha de creación original para no perderla
    original_created_at = products_db[product_id].get("created_at", datetime.now())

    updated_service = {
        "id": product_id,
        **product_update.dict(),
        "created_at": original_created_at,
        "updated_at": datetime.now() # Registramos el momento de la actualización
    }
    
    # Guardar los cambios en el almacenamiento persistente
    products_db[product_id] = updated_service

    # 4. Retornar el producto actualizado con los datos de su categoría
    response_data = updated_service.copy()
    response_data["category"] = categories_db.get(product_update.category_id)

    return response_data


# ============================================
# PATCH /products/{id} - Actualizar parcial
# ============================================

@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int = Path(..., gt=0, title="ID del Servicio", description="ID del servicio que se desea modificar"),
    product_update: ProductUpdate = ...
):
    """
    Actualiza de manera parcial los campos de un servicio de traducción.
    
    Proceso:
    1. Localiza el servicio existente.
    2. Si se intenta cambiar la categoría, valida su existencia.
    3. Modifica únicamente los atributos enviados en la solicitud.
    4. Actualiza la marca de tiempo de modificación.
    """
    
    # 1. Verificar que el producto existe (404 si no se encuentra)
    if product_id not in products_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede modificar: El servicio con ID {product_id} no existe en el sistema."
        )

    # Recuperar la información actual del servicio
    current_service_data = products_db[product_id]

    # 2. Si se proporciona category_id, verificar que existe (400 si es inválida)
    # Convertimos los datos de actualización a diccionario omitiendo los valores no enviados
    update_data = product_update.dict(exclude_unset=True)

    if "category_id" in update_data:
        new_category_id = update_data["category_id"]
        if new_category_id not in categories_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Categoría no válida: El ID de categoría {new_category_id} no existe."
            )

    # 3. Actualizar solo campos proporcionados (Patch logic)
    # Fusionamos los datos actuales con los nuevos datos parciales
    updated_service = {
        **current_service_data,
        **update_data,
        "updated_at": datetime.now() # Actualizamos la fecha de modificación
    }
    
    # Guardar los cambios en el almacenamiento persistente
    products_db[product_id] = updated_service

    # 4. Retornar el producto actualizado con la información de su categoría
    response_data = updated_service.copy()
    category_id = updated_service.get("category_id")
    response_data["category"] = categories_db.get(category_id)

    return response_data


# ============================================
# DELETE /products/{id} - Eliminar
# ============================================

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int = Path(..., gt=0, title="ID del Servicio", description="ID del servicio de traducción que se desea eliminar")
):
    """
    Elimina permanentemente un servicio de traducción del catálogo.
    
    Proceso:
    1. Verifica si el servicio existe en la base de datos.
    2. Si existe, procede con la eliminación física del registro.
    3. Si no existe, informa al usuario con un error 404.
    """
    
    # 1. Verificar que el producto existe (404 si no se encuentra)
    # Es fundamental validar antes de intentar borrar para dar feedback claro al usuario.
    if product_id not in products_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error al eliminar: El servicio con ID {product_id} no existe en nuestro catálogo."
        )

    # 2. Eliminar de products_db (Technical operation)
    # Removemos el registro de la estructura de datos persistente.
    del products_db[product_id]

    # 3. Retornar None
    # Al usar status_code 204, FastAPI automáticamente ignora cualquier retorno 
    # y envía una respuesta vacía, que es el estándar para eliminaciones exitosas.
    return None