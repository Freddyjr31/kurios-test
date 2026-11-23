from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.teachers.datasources.bd.teachers_datasource import TeachersDatasource
from app.features.teachers.repository.teachers_repository_impl import TeachersRepositoryImpl
from app.features.teachers.repository.teachers_repository_interface import (
    TeachersRepositoryInterface,
)
from app.features.teachers.use_cases.teachers_use_cases import TeachersUseCase


def get_teacher_datasource(
    db: Annotated[Session, Depends(get_db)]
) -> TeachersDatasource:
    return TeachersDatasource(db)


def get_teacher_repository(
    datasource: Annotated[TeachersDatasource, Depends(get_teacher_datasource)]
) -> TeachersRepositoryInterface:
    return TeachersRepositoryImpl(datasource)


def get_teacher_use_case(
    repository: Annotated[TeachersRepositoryInterface, Depends(get_teacher_repository)]
) -> TeachersUseCase:
    return TeachersUseCase(repository)
