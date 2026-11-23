
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request, status

from app.features.schools.schemas.schools_schemas import SchoolsResponse
from app.features.schools.dependencies import get_school_use_case
from app.features.schools.use_cases.schools_use_cases import SchoolsUseCase
from app.core.logger import logger

router = APIRouter(
    prefix="/schools",
    tags=["schools"],
)

@router.get(
    "", 
    status_code=status.HTTP_200_OK,
    response_model=SchoolsResponse,
    summary="Obtener todas las escuelas",
    description="Endpoint para obtener todas las escuelas."
    )
async def get_all_schools(
    use_case: Annotated[SchoolsUseCase, Depends(get_school_use_case)],
    name: Annotated[str | None, Query(min_length=2, max_length=20, description="Nombre de la escuela a buscar")] = None,
    limit: Annotated[int, Query(ge=1, le=100, description="Tamaño de página")] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    """
    Endpoint para obtener todas las escuelas.

    :param request: Objeto Request de FastAPI.
    :return: Lista de todas las escuelas.
    """
    
    logger.info("Obteniendo todas las escuelas")
    logger.info("Listando escuelas name=%s limit=%s offset=%s", name, limit, offset)
    # llamo el caso de uso para obtener todas las escuelas
    return use_case.get_all_schools(name=name, limit=limit, offset=offset)
    
    