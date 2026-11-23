from fastapi import FastAPI

from app.features.schools.routes.schools_routes import router as schools_router
from app.features.teachers.routes.teachers_routes import router as teachers_router
from app.features.visits.routes.visits_routes import router as visits_router

def init_routes(app: FastAPI) -> None:
    """
    Inicializa las rutas de la aplicación FastAPI.
    """
    app.include_router(schools_router)
    app.include_router(teachers_router)
    app.include_router(visits_router)