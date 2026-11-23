from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.core.logger import logger
from app.features.teachers.dependencies import get_teacher_use_case
from app.features.teachers.schemas.teachers_schemas import TeachersResponse
from app.features.teachers.use_cases.teachers_use_cases import TeachersUseCase

router = APIRouter(
    prefix="/teachers",
    tags=["teachers"],
)

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=TeachersResponse,
    summary="Obtener los maestros de un colegio",
    description="Devuelve los maestros de un colegio. Permite filtrar por nombre o apellido.",
)
def get_teachers_by_school(
    use_case: Annotated[TeachersUseCase, Depends(get_teacher_use_case)],
    school_id: Annotated[int, Query(ge=1, description="ID del colegio (obligatorio)")],
    name: Annotated[
        str | None,
        Query(min_length=2, max_length=100, description="Filtro por nombre o apellido"),
    ] = None,
    limit: Annotated[int, Query(ge=1, le=100, description="Tamaño de página")] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> TeachersResponse:
    
    """
    Endpoint para obtener los maestros de un colegio.

    :param school_id: ID del colegio a consultar.
    :param name: Texto a buscar en el nombre, apellido o nombre completo.
    :return: Maestros del colegio que cumplen el filtro.
    """
    
    logger.info(
        "Listando maestros id_school=%s name=%s limit=%s offset=%s",
        school_id,
        name,
        limit,
        offset,
    )
    
    return use_case.get_teachers_by_school(
        school_id=school_id,
        name=name,
        limit=limit,
        offset=offset,
    )
