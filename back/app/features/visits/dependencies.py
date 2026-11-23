from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.visits.datasources.bd.visits_datasource import VisitsDatasource
from app.features.visits.repository.visits_repository_impl import VisitsRepositoryImpl
from app.features.visits.repository.visits_repository_interface import (
    VisitsRepositoryInterface,
)
from app.features.visits.use_cases.visits_use_cases import VisitsUseCase


def get_visits_datasource(db: Annotated[Session, Depends(get_db)]) -> VisitsDatasource:
    return VisitsDatasource(db)


def get_visits_repository(
    datasource: Annotated[VisitsDatasource, Depends(get_visits_datasource)],
) -> VisitsRepositoryInterface:
    return VisitsRepositoryImpl(datasource)


def get_visits_use_case(
    repository: Annotated[VisitsRepositoryInterface, Depends(get_visits_repository)],
) -> VisitsUseCase:
    return VisitsUseCase(repository)
