"""
API de Catálogo de Productos - Main
===================================

Punto de entrada de la aplicación.
"""

from fastapi import FastAPI
from routers import products_router, categories_router

app = FastAPI(
    title="API de catálogo de servicios de traducción profesional",
    description="API completa con CRUD, filtrado, paginación y ordenamiento",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir routers
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(categories_router, prefix="/categories", tags=["Categories"])


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "API de Catálogo de servicios de traducción profesiona",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Root"])
async def health_check():
    """Health check"""
    return {"status": "healthy"}
