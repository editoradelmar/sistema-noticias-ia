"""
Cache Service usando Redis
backend/core/cache.py
"""
import json
from typing import Optional, Any
import logging

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logging.warning("redis no está instalado. Cache deshabilitado.")

from config import settings

logger = logging.getLogger(__name__)


class CacheService:
    """Servicio de caché usando Redis"""
    
    def __init__(self):
        """Inicializa conexión a Redis"""
        if not REDIS_AVAILABLE or not settings.CACHE_ENABLED:
            self.redis = None
            logger.warning("Cache deshabilitado")
            return
        
        try:
            self.redis = redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            logger.info("✓ Conexión a Redis establecida")
        except Exception as e:
            logger.error(f"Error conectando a Redis: {str(e)}")
            self.redis = None
    
    async def get(self, key: str) -> Optional[str]:
        """
        Obtiene un valor del cache
        
        Args:
            key: Clave del cache
        
        Returns:
            Valor o None si no existe
        """
        if not self.redis:
            return None
        
        try:
            value = await self.redis.get(key)
            if value:
                logger.debug(f"Cache hit: {key}")
            return value
        except Exception as e:
            logger.error(f"Error obteniendo de cache: {str(e)}")
            return None
    
    async def set(
        self,
        key: str,
        value: str,
        ttl: int = 3600
    ) -> bool:
        """
        Guarda un valor en el cache
        
        Args:
            key: Clave
            value: Valor
            ttl: Tiempo de vida en segundos
        
        Returns:
            True si se guardó correctamente
        """
        if not self.redis:
            return False
        
        try:
            await self.redis.setex(key, ttl, value)
            logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Error guardando en cache: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """
        Elimina una clave del cache
        
        Args:
            key: Clave a eliminar
        
        Returns:
            True si se eliminó
        """
        if not self.redis:
            return False
        
        try:
            await self.redis.delete(key)
            logger.debug(f"Cache delete: {key}")
            return True
        except Exception as e:
            logger.error(f"Error eliminando de cache: {str(e)}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Verifica si una clave existe"""
        if not self.redis:
            return False
        
        try:
            return bool(await self.redis.exists(key))
        except Exception as e:
            logger.error(f"Error verificando cache: {str(e)}")
            return False
    
    async def clear_pattern(self, pattern: str) -> int:
        """
        Elimina todas las claves que coincidan con un patrón
        
        Args:
            pattern: Patrón (ej: "user:*")
        
        Returns:
            Número de claves eliminadas
        """
        if not self.redis:
            return 0
        
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                return await self.redis.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Error limpiando cache: {str(e)}")
            return 0
    
    async def get_json(self, key: str) -> Optional[Any]:
        """Obtiene un objeto JSON del cache"""
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                logger.error(f"Error decodificando JSON de cache: {key}")
        return None
    
    async def set_json(
        self,
        key: str,
        value: Any,
        ttl: int = 3600
    ) -> bool:
        """Guarda un objeto JSON en el cache"""
        try:
            json_str = json.dumps(value)
            return await self.set(key, json_str, ttl)
        except (TypeError, ValueError) as e:
            logger.error(f"Error codificando JSON para cache: {str(e)}")
            return False
    
    async def close(self):
        """Cierra la conexión a Redis"""
        if self.redis:
            await self.redis.close()
            logger.info("✓ Conexión a Redis cerrada")


# Instancia global
_cache_service = None


def get_cache_service() -> CacheService:
    """Obtiene la instancia global del cache service"""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service
