"""
Router de Categorías
====================

CRUD completo para categorías.

TODO: Implementa los endpoints siguiendo las instrucciones.
"""

from fastapi import APIRouter, Path, HTTPException, status
from datetime import datetime

from database import categories_db, get_next_category_id
from schemas import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    responses={404: {"description": "Categoria no definida"}}
)


# ============================================
# GET /categories - Listar todas
# ============================================

@router.get("/", response_model=list[CategoryResponse])
async def list_categories():
    """
    Obtiene la lista completa de especialidades de traducción disponibles.
    
    Retorna todas las categorías registradas en el sistema (ej. Traducción Jurada, 
    Localización de Software, Traducción Literaria).
    """
    # 1. Recuperar los valores del diccionario de la base de datos
    # Convertimos la estructura de datos interna a una lista compatible con el esquema de respuesta
    categories_list = list(categories_db.values())
    
    # 2. Retornar los datos
    # FastAPI se encarga de validar cada objeto contra el CategoryResponse
    return categories_list

# ============================================
# GET /categories/{id} - Obtener una
# ============================================

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int = Path(..., gt=0, title="ID de la Categoría", description="Identificador único de la especialidad de traducción")
):
    """
    Obtener el detalle de una categoría de traducción por su ID.
    
    Proceso:
    1. Busca la categoría en la base de datos interna.
    2. Si no se encuentra, devuelve un error descriptivo.
    3. Retorna los datos de la especialidad (nombre, descripción, etc.).
    """
    
    # 1. Buscar en categories_db (Lógica interna en inglés)
    category = categories_db.get(category_id)
    
    # 2. Validación y manejo de error 404
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La categoría de traducción con ID {category_id} no existe en nuestros registros."
        )
    
    # 3. Retornar la categoría encontrada
    return category


# ============================================
# POST /categories - Crear
# ============================================

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate):
    """
    Registra una nueva categoría o especialidad de traducción en el sistema.
    
    Proceso:
    1. Genera un identificador único para la nueva categoría.
    2. Registra la fecha y hora exacta de creación.
    3. Almacena la especialidad (ej. Traducción Financiera, Interpretación Simultánea).
    4. Retorna el objeto creado con su ID asignado.
    """
    
    # 1. Obtener nuevo ID (Technical operation)
    new_category_id = get_next_category_id()
    
    # 2. Crear diccionario con los metadatos necesarios
    # Combinamos el ID generado, los campos del esquema y el timestamp de creación
    new_category_record = {
        "id": new_category_id,
        **category_data.dict(),
        "created_at": datetime.now()
    }
    
    # 3. Guardar en la base de datos (Persistencia en memoria)
    categories_db[new_category_id] = new_category_record
    
    # 4. Retornar la categoría creada
    # FastAPI validará este diccionario contra el esquema CategoryResponse
    return new_category_record


# ============================================
# PUT /categories/{id} - Actualizar completo
# ============================================

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int = Path(..., gt=0, title="ID de la Categoría", description="ID de la especialidad que se desea reemplazar"),
    category_data: CategoryCreate = ...
):
    """
    Reemplaza íntegramente los datos de una categoría de traducción existente.
    
    Proceso:
    1. Valida si la categoría existe en el sistema.
    2. Sobrescribe todos los atributos con la nueva información proporcionada.
    3. Mantiene la integridad del ID original.
    4. Retorna la categoría con los cambios aplicados.
    """
    
    # 1. Verificar si la categoría existe (404 si no se encuentra)
    if category_id not in categories_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No es posible actualizar: La categoría con ID {category_id} no existe."
        )

    # 2. Actualizar todos los campos (Full replacement logic)
    # Recuperamos la fecha de creación original para preservarla en el nuevo objeto
    original_created_at = categories_db[category_id].get("created_at", datetime.now())

    updated_category_record = {
        "id": category_id,
        **category_data.dict(),
        "created_at": original_created_at,
        "updated_at": datetime.now()  # Registramos la fecha de modificación técnica
    }
    
    # Guardar los cambios en el almacenamiento persistente
    categories_db[category_id] = updated_category_record

    # 3. Retornar la categoría actualizada
    return updated_category_record


# ============================================
# DELETE /categories/{category_id} - Eliminar
# ============================================

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int = Path(..., gt=0, title="ID de la Categoría", description="ID de la especialidad que se desea eliminar")
):
    """
    Elimina permanentemente una categoría de traducción del sistema.
    
    Proceso:
    1. Valida si la categoría existe en la base de datos.
    2. Si existe, elimina el registro por completo.
    3. Si no existe, lanza un error 404 para informar al usuario.
    4. Retorna una respuesta vacía (204 No Content) tras una operación exitosa.
    """
    
    # 1. Verificar que la categoría existe (404 si no se encuentra)
    # Buscamos en el diccionario técnico de categorías
    if category_id not in categories_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Operación fallida: La categoría con ID {category_id} no existe y no puede ser eliminada."
        )

    # 2. Eliminar de categories_db (Operación técnica de borrado)
    # Eliminamos la llave del diccionario en memoria
    del categories_db[category_id]

    # 3. Retornar None
    # FastAPI gestiona automáticamente el status 204 omitiendo el cuerpo de la respuesta
    return None