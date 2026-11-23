from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from app.features.visits.enums import TypeVisitEnum, VisitStatusEnum
from app.features.visits.exceptions import (
    SchoolNotFoundError,
    TeacherNotFoundError,
    VisitConflictError,
    VisitNotFoundError,
    VisitValidationError,
)
from app.features.visits.models.visits_models import SchoolVisitModel
from app.features.visits.repository.visits_repository_interface import (
    VisitsRepositoryInterface,
)
from app.features.visits.schemas.visits_schemas import (
    VisitBaseResponse,
    VisitCreateRequest,
    VisitListItemResponse,
    VisitUpdateRequest,
    VisitsResponse,
)

CARACAS_TZ = ZoneInfo("America/Caracas")

#: Campos editables que nunca pueden quedar en NULL.
REQUIRED_EDITABLE_FIELDS = (
    "id_school",
    "id_teacher",
    "date_visit",
    "time_visit",
    "type_visit",
)


class VisitsUseCase:

    def __init__(self, repository: VisitsRepositoryInterface):
        self.repository = repository

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def get_type_visits(self) -> list[str]:
        """
        Devuelve los tipos de visita disponibles para registrar una visita.
        """
        return self.repository.get_type_visits()

    def get_visits(
        self,
        *,
        school_id: int | None = None,
        type_visit: TypeVisitEnum | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> VisitsResponse:
        """
        Devuelve las visitas visibles que cumplen los filtros, con su total real.
        """
        type_value = type_visit.value if type_visit is not None else None

        visits = self.repository.get_visits(
            school_id=school_id,
            type_visit=type_value,
            limit=limit,
            offset=offset,
        )
        total = self.repository.count_visits(
            school_id=school_id, type_visit=type_value
        )

        return VisitsResponse(
            visits=[VisitListItemResponse.from_row(row) for row in visits],
            total=total,
            limit=limit,
            offset=offset,
        )

    # ------------------------------------------------------------------
    # Escrituras
    # ------------------------------------------------------------------

    def create_visit(self, payload: VisitCreateRequest) -> VisitBaseResponse:
        """
        Registra una visita validando colegio, profesor, fecha y disponibilidad.
        """
        self._ensure_school_exists(payload.id_school)
        self._ensure_teacher_in_school(payload.id_teacher, payload.id_school)
        self._ensure_not_future(payload.date_visit, payload.time_visit)
        self._ensure_slot_free(
            teacher_id=payload.id_teacher,
            date_visit=payload.date_visit,
            time_visit=payload.time_visit,
        )

        visit = SchoolVisitModel(
            id_school=payload.id_school,
            id_teacher=payload.id_teacher,
            date_visit=payload.date_visit,
            time_visit=payload.time_visit,
            notes=self._normalize_notes(payload.notes),
            type_visit=payload.type_visit.value,
            visit_status=VisitStatusEnum.VISIBLE.value,
        )

        created = self.repository.create_visit(visit)
        return VisitBaseResponse.model_validate(created)

    def update_visit(
        self, visit_id: int, payload: VisitUpdateRequest
    ) -> VisitBaseResponse:
        """
        Edita parcialmente una visita visible, revalidando la relación
        profesor/colegio, la fecha y la disponibilidad con los valores finales.
        """
        visit = self.repository.get_visit(visit_id)

        if visit is None or visit.visit_status == VisitStatusEnum.HIDE.value:
            raise VisitNotFoundError("Visita no encontrada")

        changes = payload.model_dump(exclude_unset=True)

        for field in REQUIRED_EDITABLE_FIELDS:
            if field in changes and changes[field] is None:
                raise VisitValidationError(
                    f"El campo '{field}' no puede ser nulo"
                )

        id_school = changes.get("id_school", visit.id_school)
        id_teacher = changes.get("id_teacher", visit.id_teacher)
        date_visit = changes.get("date_visit", visit.date_visit)
        time_visit = changes.get("time_visit", visit.time_visit)

        if id_school is None or id_teacher is None:
            raise VisitValidationError("La visita debe tener colegio y profesor")

        if "id_school" in changes:
            self._ensure_school_exists(id_school)

        self._ensure_teacher_in_school(id_teacher, id_school)
        self._ensure_not_future(date_visit, time_visit)
        self._ensure_slot_free(
            teacher_id=id_teacher,
            date_visit=date_visit,
            time_visit=time_visit,
            exclude_visit_id=visit_id,
        )

        if "notes" in changes:
            changes["notes"] = self._normalize_notes(changes["notes"])
        if "type_visit" in changes:
            changes["type_visit"] = changes["type_visit"].value

        updated = self.repository.update_visit(visit_id, changes)

        if updated is None:
            raise VisitNotFoundError("Visita no encontrada")

        return VisitBaseResponse.model_validate(updated)

    def soft_delete_visit(self, visit_id: int) -> None:
        """
        Oculta una visita en lugar de eliminarla físicamente.

        :param visit_id: ID de la visita a ocultar.
        """
        if not self.repository.soft_delete_visit(visit_id):
            raise VisitNotFoundError("Visita no encontrada")

    # ------------------------------------------------------------------
    # Validaciones internas
    # ------------------------------------------------------------------

    def _ensure_school_exists(self, school_id: int) -> None:
        if not self.repository.school_exists(school_id):
            raise SchoolNotFoundError("Colegio no encontrado")

    def _ensure_teacher_in_school(self, teacher_id: int, school_id: int) -> None:
        teacher_school = self.repository.get_teacher_school(teacher_id)

        if teacher_school is None:
            raise TeacherNotFoundError("Profesor no encontrado")

        if teacher_school != school_id:
            raise VisitValidationError(
                "El profesor no pertenece al colegio indicado"
            )

    def _ensure_not_future(self, date_visit: date | None, time_visit: time | None) -> None:
        """
        Rechaza visitas con fecha y hora posteriores al momento actual.

        `date_visit` y `time_visit` son hora local de Venezuela y el servidor
        puede estar en otra zona, así que la comparación se hace explícitamente
        en `America/Caracas`.
        """
        if date_visit is None or time_visit is None:
            return

        visit_at = datetime.combine(date_visit, time_visit, tzinfo=CARACAS_TZ)

        if visit_at > datetime.now(CARACAS_TZ):
            raise VisitValidationError(
                "La fecha y hora de la visita no puede ser futura"
            )

    def _ensure_slot_free(
        self,
        *,
        teacher_id: int | None,
        date_visit: date | None,
        time_visit: time | None,
        exclude_visit_id: int | None = None,
    ) -> None:
        """
        Impide que un profesor tenga dos visitas visibles a la misma hora.
        Puede haber varias visitas al mismo colegio si son profesores distintos.
        """
        if teacher_id is None or date_visit is None or time_visit is None:
            return

        if self.repository.exists_visit_at(
            teacher_id=teacher_id,
            date_visit=date_visit,
            time_visit=time_visit,
            exclude_visit_id=exclude_visit_id,
        ):
            raise VisitConflictError(
                "El profesor ya tiene una visita registrada en esa fecha y hora"
            )

    @staticmethod
    def _normalize_notes(notes: str | None) -> str | None:
        if notes is None:
            return None

        cleaned = notes.strip()
        return cleaned or None
