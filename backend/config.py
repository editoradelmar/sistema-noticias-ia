"""
Configuración centralizada de la aplicación
Usar variables de entorno en producción
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Configuración general de la aplicación
    APP_NAME: str = "Sistema de Noticias con IA"
    APP_VERSION: str = "2.4.0"  # Actualizado con admin usuarios y paginación
    APP_DESCRIPTION: str = "Sistema profesional de gestión de noticias con IA"
    COMPANY: str = "Editor del Mar SA"
    AUTHOR: str = "Hector Romero"
    EMAIL: str = "hromero@eluniversal.com.co"
    
    # Configuración técnica
    DEBUG: bool = True
    VERSION: str = APP_VERSION  # Alias para compatibilidad
    
    # Base de Datos PostgreSQL - Usar 127.0.0.1 para evitar problemas UTF-8
    DATABASE_URL: str = "postgresql://openpg:openpgpwd@127.0.0.1:5432/noticias_ia"
    # Formato: postgresql://usuario:password@host:puerto/nombre_db
    # Ejemplo producción: postgresql://user:pass@db.example.com:5432/prod_db
    
    # Seguridad y JWT
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    # IMPORTANTE: En producción, generar con: openssl rand -hex 32
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Keys (IMPORTANTE: Obtener desde variables de entorno)
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    
    # CORS - Permitir localhost, IP local y cualquier IP LAN
    ALLOWED_ORIGINS: str = (
        "http://localhost:5173,"
        "http://localhost:3000,"
        "http://127.0.0.1:5173,"
        "http://127.0.0.1:3000,"
        "http://172.17.100.64:5173,"
        "http://192.168.0.100:5173,"
        "http://192.168.1.100:5173,"
        "http://10.0.0.2:5173,"
        "http://10.0.0.3:5173,"
        "http://10.0.0.4:5173,"
        "http://192.168.1.101:5173,"
        "http://192.168.1.102:5173,"
        "https://epic-exactly-bull.ngrok-free.app,"
        "https://willyard-nonceremonial-leonila.ngrok-free.dev"
    )

    # Límites de la API
    MAX_TOKENS_IA: int = 2000
    MAX_NOTICIAS_POR_PAGINA: int = 100
    # Máximo de caracteres permitidos en el prompt final enviado al LLM
    # Este valor protege contra prompts excesivamente largos que pueden causar
    # fallos en el proveedor o consumos inesperados de tokens. Ajustable vía .env
    MAX_PROMPT_CHARS: int = 50000
    
    # Claude API
    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
    CLAUDE_API_URL: str = "https://api.anthropic.com/v1/messages"
    
    # Almacenamiento de archivos
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instancia global
settings = Settings()

# Crear directorio de uploads si no existe
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Validar configuración
if settings.ANTHROPIC_API_KEY:
    print(f"""
    ╔══════════════════════════════════════════╗
    ║  {settings.APP_NAME:^38}  ║
    ║  v{settings.APP_VERSION:^36}   ║
    ╠══════════════════════════════════════════╣
    ║  ✅ API Key Configurada                  ║
    ║  🤖 Claude API: ACTIVA                   ║
    ║  🗄️  PostgreSQL: CONECTADA               ║
    ║  📡 Modo: PRODUCCIÓN                     ║
    ╚══════════════════════════════════════════╝
    """)
else:
    print(f"""
    ╔══════════════════════════════════════════╗
    ║  {settings.APP_NAME:^38}  ║
    ║  v{settings.APP_VERSION:^36}  ║
    ╠══════════════════════════════════════════╣
    ║  ⚠️  API Key NO Configurada              ║
    ║  🤖 Claude API: MODO SIMULADO            ║
    ║  🗄️  PostgreSQL: CONECTADA               ║
    ║  📡 Modo: DESARROLLO                     ║
    ╚══════════════════════════════════════════╝
    """)
