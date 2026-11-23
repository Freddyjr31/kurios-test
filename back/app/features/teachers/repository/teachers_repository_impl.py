from app.features.teachers.datasources.bd.teachers_datasource import TeachersDatasource
from app.features.teachers.models.teachers_models import TeacherModel
from app.features.teachers.repository.teachers_repository_interface import (
    TeachersRepositoryInterface,
)


class TeachersRepositoryImpl(TeachersRepositoryInterface):
    
    def __init__(self, datasource: TeachersDatasource):
        self.datasource = datasource

    def get_teachers(
        self,
        *,
        school_id: int,
        name: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[TeacherModel]:
        """
        Obtiene los maestros de un colegio desde la fuente de datos.
        """
        return self.datasource.get_teachers(
            school_id=school_id,
            name=name,
            limit=limit,
            offset=offset,
        )

    def count_teachers(self, *, school_id: int, name: str | None = None) -> int:
        """
        Cuenta los maestros de un colegio desde la fuente de datos.
        """
        return self.datasource.count_teachers(school_id=school_id, name=name)
