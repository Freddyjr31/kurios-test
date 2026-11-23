from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from app.core.logger import logger
from app.features.visits.dependencies import get_visits_use_case
from app.features.visits.enums import TypeVisitEnum
from app.features.visits.schemas.visits_schemas import (
    VisitBaseResponse,
    VisitCreateRequest,
    VisitUpdateRequest,
    VisitsResponse,
)
from app.features.visits.use_cases.visits_use_cases import VisitsUseCase

router = APIRouter(
    prefix="/visits",
    tags=["visits"],
)


@router.get(
    "/types",
    status_code=status.HTTP_200_OK,
    response_model=list[str],
    summary="Obtener los tipos de visita",
    description="Devuelve los valores del enum `type_visits_enum` en el orden definido en la base de datos.",
)
def get_type_visits(
    use_case: Annotated[VisitsUseCase, Depends(get_visits_use_case)],
) -> list[str]:
    """
    Endpoint para obtener los tipos de visita disponibles al registrar una visita.

    :return: Lista de tipos de visita, por ejemplo `["En Aula", "Encuentro"]`.
    """
    logger.info("Listando tipos de visita")
    return use_case.get_type_visits()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=VisitsResponse,
    summary="Obtener las visitas",
    description=(
        "Devuelve las visitas visibles, de la más reciente a la más antigua. "
        "Incluye el nombre del colegio y del profesor."
    ),
)
def get_visits(
    use_case: Annotated[VisitsUseCase, Depends(get_visits_use_case)],
    school_id: Annotated[
        int | None, Query(ge=1, description="ID del colegio")
    ] = None,
    type_visit: Annotated[
        TypeVisitEnum | None, Query(description="Tipo de visita")
    ] = None,
    limit: Annotated[int, Query(ge=1, le=100, description="Tamaño de página")] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> VisitsResponse:
    """
    Endpoint para obtener las visitas según los filtros proporcionados.

    :param school_id: ID del colegio.
    :param type_visit: Tipo de visita.
    :param limit: Número máximo de resultados a devolver.
    :param offset: Número de resultados a omitir.
    :return: Visitas que coinciden con los criterios y el total real.
    """
    logger.info(
        "Listando visitas school_id=%s type_visit=%s limit=%s offset=%s",
        school_id,
        type_visit,
        limit,
        offset,
    )

    return use_case.get_visits(
        school_id=school_id,
        type_visit=type_visit,
        limit=limit,
        offset=offset,
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=VisitBaseResponse,
    summary="Crear una nueva visita",
    description=(
        "Registra una visita. La fecha y hora no pueden ser futuras y un "
        "profesor no puede tener dos visitas a la misma hora."
    ),
)
def create_visit(
    use_case: Annotated[VisitsUseCase, Depends(get_visits_use_case)],
    payload: VisitCreateRequest,
) -> VisitBaseResponse:
    """
    Endpoint para crear una nueva visita.

    :param payload: Datos de la visita a registrar.
    :return: La visita creada con su ID asignado.
    """
    logger.info(
        "Creando visita id_school=%s id_teacher=%s date_visit=%s time_visit=%s",
        payload.id_school,
        payload.id_teacher,
        payload.date_visit,
        payload.time_visit,
    )
    return use_case.create_visit(payload)


@router.patch(
    "/{visit_id}",
    status_code=status.HTTP_200_OK,
    response_model=VisitBaseResponse,
    summary="Editar una visita",
    description=(
        "Edita parcialmente una visita visible. Envía solo los campos que "
        "quieres cambiar."
    ),
)
def update_visit(
    use_case: Annotated[VisitsUseCase, Depends(get_visits_use_case)],
    visit_id: Annotated[int, Path(ge=1, description="ID de la visita a editar")],
    payload: VisitUpdateRequest,
) -> VisitBaseResponse:
    """
    Endpoint para actualizar una visita existente.

    :param visit_id: ID de la visita a actualizar.
    :param payload: Campos a modificar.
    :return: La visita actualizada.
    """
    logger.info("Actualizando visita id=%s campos=%s", visit_id, payload.model_fields_set)
    return use_case.update_visit(visit_id, payload)


@router.delete(
    "/{visit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Ocultar una visita",
    description=(
        "No elimina la visita: cambia su estado a `hide` para conservar la "
        "transacción histórica. La operación es idempotente."
    ),
)
def soft_delete_visit(
    use_case: Annotated[VisitsUseCase, Depends(get_visits_use_case)],
    visit_id: Annotated[int, Path(ge=1, description="ID de la visita a ocultar")],
) -> None:
    """
    Endpoint para ocultar (soft delete) una visita.

    :param visit_id: ID de la visita a ocultar.
    """
    logger.info("Ocultando visita id=%s", visit_id)
    use_case.soft_delete_visit(visit_id)
