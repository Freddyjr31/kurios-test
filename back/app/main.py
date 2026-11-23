from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings, VERSION
from app.core.database import Base, get_engine
from app.features.visits.exceptions import VisitsError
from app.routes.routes import init_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=get_engine())
    yield
    
app = FastAPI(
    title="Kurios visits API",
    description="Este proyecto es un ejemplo de API RESTful construida con FastAPI, para gestionar visitas realizadas a los colegios dentro de la plataforma Kurios. Proporciona endpoints para crear, leer, actualizar y eliminar registros de visitas.",
    version=VERSION,
    lifespan=lifespan,
)

settings = get_settings()
is_production = settings.ENV == "production"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Inicializar las rutas de la aplicación
init_routes(app)


@app.exception_handler(VisitsError)
async def visits_error_handler(request: Request, exc: VisitsError) -> JSONResponse:
    """
    Traduce los errores de negocio de `visits` al código HTTP que define
    cada excepción.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Endpoint raíz para verificar que la API está en funcionamiento
@app.get("/")
async def root():
    return {"message": "Kurios visits API is running!"}