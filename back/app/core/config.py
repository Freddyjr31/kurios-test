from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

#? ----- Project version
VERSION = "1.0.2"

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")
    
    #? ──────────────────────────────────────────────
    #?               Entorno
    #? ──────────────────────────────────────────────

    # "development" | "production"
    # En producción se desactivan /docs, /redoc y /openapi.json
    ENV: str = "development"

    #? ──────────────────────────────────────────────
    #?        Configuración de base de datos
    #? ──────────────────────────────────────────────

    # URL de conexión a la base de datos principal
    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost/dbname"

    # Tipo de base de datos: "postgresql" | "sqlite" | "mysql"
    DATABASE_TYPE: str = "postgresql"

    # Activar logs detallados de SQLAlchemy (útil en desarrollo)
    DATABASE_ECHO: bool = False
    
    HTTP_TIMEOUT_SECONDS: int = 10
    HTTP_MAX_RETRIES: int = 3


# @lru_cache asegura que la instancia de Settings se cree una sola vez
# y se reutilice en toda la aplicación, mejorando el rendimiento.
@lru_cache()
def get_settings():
    s = Settings()
    assert s.HTTP_TIMEOUT_SECONDS > 0, "HTTP_TIMEOUT_SECONDS debe ser > 0"
    return s