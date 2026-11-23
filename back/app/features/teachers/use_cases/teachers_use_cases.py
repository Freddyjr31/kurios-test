from app.features.teachers.repository.teachers_repository_interface import (
    TeachersRepositoryInterface,
)
from app.features.teachers.schemas.teachers_schemas import (
    TeacherBaseResponse,
    TeachersResponse,
)


class TeachersUseCase:

    def __init__(self, repository: TeachersRepositoryInterface):
        self.repository = repository

    def get_teachers_by_school(
        self,
        *,
        school_id: int,
        name: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> TeachersResponse:

        name = name.strip() if name else None

        teachers = self.repository.get_teachers(
            school_id=school_id,
            name=name,
            limit=limit,
            offset=offset,
        )
        total = self.repository.count_teachers(school_id=school_id, name=name)

        return TeachersResponse(
            teachers=[TeacherBaseResponse.model_validate(teacher) for teacher in teachers],
            total=total,
            limit=limit,
            offset=offset,
        )
