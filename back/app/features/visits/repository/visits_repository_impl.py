from datetime import date, time

from app.features.visits.datasources.bd.visits_datasource import VisitsDatasource
from app.features.visits.models.visits_models import SchoolVisitModel, VisitWithNames
from app.features.visits.repository.visits_repository_interface import (
    VisitsRepositoryInterface,
)


class VisitsRepositoryImpl(VisitsRepositoryInterface):
    def __init__(self, datasource: VisitsDatasource):
        self.datasource = datasource

    def get_type_visits(self) -> list[str]:
        """
        Obtiene los tipos de visita desde la fuente de datos.
        """
        return self.datasource.get_type_visits()

    def get_visits(
        self,
        *,
        school_id: int | None = None,
        type_visit: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[VisitWithNames]:
        """
        Obtiene las visitas desde la fuente de datos.
        """
        return self.datasource.get_visits(
            school_id=school_id,
            type_visit=type_visit,
            limit=limit,
            offset=offset,
        )

    def count_visits(
        self,
        *,
        school_id: int | None = None,
        type_visit: str | None = None,
    ) -> int:
        """
        Cuenta las visitas desde la fuente de datos.
        """
        return self.datasource.count_visits(
            school_id=school_id, type_visit=type_visit
        )

    def get_visit(self, visit_id: int) -> SchoolVisitModel | None:
        """
        Obtiene una visita por ID desde la fuente de datos.
        """
        return self.datasource.get_visit(visit_id)

    def school_exists(self, school_id: int) -> bool:
        """
        Verifica si el colegio existe.
        """
        return self.datasource.school_exists(school_id)

    def get_teacher_school(self, teacher_id: int) -> int | None:
        """
        Obtiene el colegio del profesor.
        """
        return self.datasource.get_teacher_school(teacher_id)

    def exists_visit_at(
        self,
        *,
        teacher_id: int,
        date_visit: date,
        time_visit: time,
        exclude_visit_id: int | None = None,
    ) -> bool:
        """
        Verifica si el profesor ya tiene una visita en esa fecha y hora.
        """
        return self.datasource.exists_visit_at(
            teacher_id=teacher_id,
            date_visit=date_visit,
            time_visit=time_visit,
            exclude_visit_id=exclude_visit_id,
        )

    def create_visit(self, visit: SchoolVisitModel) -> SchoolVisitModel:
        """
        Crea una visita en la fuente de datos.
        """
        return self.datasource.create_visit(visit)

    def update_visit(
        self, visit_id: int, updated_data: dict
    ) -> SchoolVisitModel | None:
        """
        Actualiza una visita en la fuente de datos.
        """
        return self.datasource.update_visit(visit_id, updated_data)

    def soft_delete_visit(self, visit_id: int) -> bool:
        """
        Oculta una visita desde la fuente de datos.
        """
        return self.datasource.soft_delete_visit(visit_id)
