"""
Sistema de Noticias con IA - FastAPI Backend v2.0
Con PostgreSQL y SQLAlchemy
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from config import settings
from core.database import init_db, engine

# Importar routers
from routers import noticias, ai, auth, proyectos
from routers import llm_maestro, prompts, estilos, secciones, salidas, generacion

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup: Inicializar base de datos
    print("🔄 Inicializando base de datos...")
    init_db()
    print("✅ Sistema inicializado correctamente")
    
    yield
    
    # Shutdown: Cerrar conexiones
    engine.dispose()
    print("🔴 Sistema apagándose...")

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Noticias con IA",
    description="API REST para gestión de noticias con integración de IA y PostgreSQL",
    version="2.0.0",
    lifespan=lifespan
)

# Mostrar valor de CORS en consola para depuración
print('CORS origins:', settings.ALLOWED_ORIGINS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.ALLOWED_ORIGINS.split(',')],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["autenticacion"])
app.include_router(proyectos.router)  # Incluye prefix en el router
app.include_router(noticias.router, prefix="/api/noticias", tags=["noticias"])
app.include_router(ai.router, prefix="/api/ai", tags=["ia"])

# Routers Fase 6 - Sistema de Maestros
app.include_router(llm_maestro.router)
app.include_router(prompts.router)
app.include_router(estilos.router)
app.include_router(secciones.router)
app.include_router(salidas.router)
app.include_router(generacion.router)  # 🎉 Nuevo - Generación IA
# Routers para manejo de items
from routers import prompt_items, estilo_items
app.include_router(prompt_items.router)
app.include_router(estilo_items.router)

# Endpoint raíz
@app.get("/")
async def root():
    return {
        "mensaje": "Sistema de Noticias con IA - API v2.0",
        "documentacion": "/docs",
        "estado": "activo",
        "database": "PostgreSQL"
    }

# Health check
@app.get("/health")
async def health_check():
    from sqlalchemy import text
    
    try:
        # Verificar conexión a BD
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "version": settings.VERSION
    }

# Ejecutar servidor
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Hot reload en desarrollo
    )
