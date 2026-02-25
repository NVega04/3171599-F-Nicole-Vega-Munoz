# 🌐 Translation Services API - FastAPI

Este proyecto es una API RESTful desarrollada con **FastAPI** para la gestión integral de una **Agencia de Traducción Profesional**. El sistema permite administrar un catálogo de servicios especializados (productos) y sus categorías de traducción (especialidades).

---

## 🚀 ¿Qué se hizo?

Se ha construido una arquitectura modular y escalable que sigue las mejores prácticas de desarrollo con Python:

* **CRUD Completo**: Implementación de operaciones de Crear, Leer, Actualizar y Borrar tanto para servicios como para categorías.
* **Filtrado Avanzado**: Sistema de búsqueda por texto, rangos de precios, disponibilidad (stock de traductores) y etiquetas técnicas.
* **Paginación y Ordenamiento**: Control de grandes volúmenes de datos mediante parámetros de desplazamiento y criterios de ordenación dinámicos.
* **Validación de Datos**: Uso intensivo de **Pydantic V2** para asegurar la integridad de la información y tipos de datos.
* **Base de Datos en Memoria**: Estructura de datos optimizada en diccionarios con funciones auxiliares para la gestión de IDs incrementales.

---

## 🏗️ Arquitectura del Proyecto

El código se organiza de forma modular para facilitar el mantenimiento:

| Archivo | Descripción |
| :--- | :--- |
| `main.py` | Punto de entrada de la aplicación y registro de rutas. |
| `database.py` | "Single Source of Truth" con datos simulados y funciones de persistencia. |
| `schemas.py` | Definición de modelos Pydantic y validación de esquemas (Request/Response). |
| `dependencies.py` | Lógica reutilizable para paginación, filtros y ordenamiento. |
| `routers/` | Directorio que contiene los endpoints divididos por dominio (`products` y `categories`). |

---

## 💼 Dominio de Negocio: Agencia de Traducción

A diferencia de un e-commerce genérico, esta API está adaptada a las necesidades de una agencia:

* **Especialidades (Categorías)**: Legal, Técnica, Médica, Localización de Software, etc.
* **Tarificación**: Los precios representan tasas por palabra o por minuto de audio/video.
* **Disponibilidad (Stock)**: Representa el número de traductores especializados disponibles para tomar un encargo de forma inmediata.
* **Etiquetas (Tags)**: Identificadores técnicos como `#urgente`, `#nativo`, `#jurado` o `#seo`.

---

## 🛠️ Tecnologías Utilizadas

* **FastAPI**: Framework moderno y rápido para construir APIs con Python 3.10+.
* **Pydantic**: Validación de datos y gestión de configuraciones.
* **Uvicorn**: Servidor ASGI de alto rendimiento.
* **Annotated Types**: Para una inyección de dependencias más limpia y tipada.

---

## 💡 Información Importante para Desarrolladores

### 🔑 Convención de Idiomas
Se ha seguido una regla estricta de **"Inglés por dentro, Español por fuera"**:
* **Código**: Variables, funciones, clases y lógica interna están en inglés técnico.
* **Documentación/UI**: Los docstrings de Swagger, mensajes de error y descripciones de parámetros están en español para facilitar la comprensión del usuario final.

### 🚩 Ejecución del Proyecto
1. Instalar dependencias: `pip install fastapi uvicorn`
2. Correr el servidor: `uvicorn main:app --reload`
3. Acceder a la documentación interactiva:
    * Swagger UI: `http://127.0.0.1:8000/docs`
    * ReDoc: `http://127.0.0.1:8000/redoc`

---
> Proyecto desarrollado como parte del módulo de APIs Modernas - Week 03.