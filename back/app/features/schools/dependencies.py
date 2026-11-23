
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.features.schools.datasources.bd.schools_datasource import SchoolsDatasource
from app.features.schools.repository.school_repository_impl import SchoolsRepositoryImpl
from app.features.schools.repository.school_repository_interface import SchoolsRepositoryInterface
from app.features.schools.use_cases.schools_use_cases import SchoolsUseCase

def get_school_datasource(
    db: Annotated[Session, Depends(get_db)]
) -> SchoolsDatasource:
    return SchoolsDatasource(db)

def get_school_repository(
    datasource: Annotated[SchoolsDatasource, Depends(get_school_datasource)]
) -> SchoolsRepositoryInterface:
    return SchoolsRepositoryImpl(datasource)

def get_school_use_case(
    repository: Annotated[SchoolsRepositoryInterface, Depends(get_school_repository)]
) -> SchoolsUseCase:
    return SchoolsUseCase(repository)