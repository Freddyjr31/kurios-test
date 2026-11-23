from datetime import date, datetime, time
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.features.visits.enums import TypeVisitEnum, VisitStatusEnum

if TYPE_CHECKING:
    from app.features.visits.models.visits_models import VisitWithNames

NOTES_MAX_LENGTH = 1000


class VisitBaseResponse(BaseModel):
    """
    Representación de una visita para las respuestas de la API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., examples=[1])
    id_school: int | None = Field(None, examples=[1])
    id_teacher: int | None = Field(None, examples=[1])
    date_visit: date | None = Field(None, examples=["2026-11-22"])
    time_visit: time | None = Field(None, examples=["09:00:00"])
    notes: str | None = Field(None, examples=["Visita de ejemplo"])
    visit_status: VisitStatusEnum | None = Field(None, examples=["visible"])
    type_visit: TypeVisitEnum | None = Field(None, examples=["En Aula"])
    created_at: datetime = Field(..., examples=["2026-11-22T09:00:00-04:00"])
    updated_at: datetime | None = Field(None, examples=["2026-11-22T09:30:00-04:00"])


class VisitListItemResponse(VisitBaseResponse):
    """
    Visita del listado, enriquecida con los nombres del colegio y del profesor
    para que el front no tenga que cruzarlos por id.
    """

    school_name: str | None = Field(None, examples=["U.E Maria Auxiliadora"])
    teacher_name: str | None = Field(None, examples=["Ana Pérez"])

    @classmethod
    def from_row(cls, row: "VisitWithNames") -> "VisitListItemResponse":
        base = VisitBaseResponse.model_validate(row.visit)
        return cls(
            **base.model_dump(),
            school_name=row.school_name,
            teacher_name=row.teacher_name,
        )


class VisitsResponse(BaseModel):
    visits: list[VisitListItemResponse] = Field(...)
    total: int = Field(..., examples=[1])
    limit: int = Field(..., examples=[20])
    offset: int = Field(..., examples=[0])


class VisitCreateRequest(BaseModel):
    """
    Datos para registrar una visita. `visit_status` no se acepta: al crear
    siempre queda `visible`.
    """

    id_school: int = Field(..., ge=1, examples=[1])
    id_teacher: int = Field(..., ge=1, examples=[1])
    date_visit: date = Field(..., examples=["2026-11-20"])
    time_visit: time = Field(..., examples=["09:00:00"])
    notes: str | None = Field(
        None, max_length=NOTES_MAX_LENGTH, examples=["Visita de seguimiento"]
    )
    type_visit: TypeVisitEnum = Field(..., examples=["En Aula"])


class VisitUpdateRequest(BaseModel):
    """
    Edición parcial: todos los campos son opcionales, pero debe venir al menos
    uno. `visit_status` se cambia solo con `DELETE /visits/{id}`.
    """

    id_school: int | None = Field(None, ge=1, examples=[1])
    id_teacher: int | None = Field(None, ge=1, examples=[1])
    date_visit: date | None = Field(None, examples=["2026-11-20"])
    time_visit: time | None = Field(None, examples=["09:00:00"])
    notes: str | None = Field(None, max_length=NOTES_MAX_LENGTH)
    type_visit: TypeVisitEnum | None = Field(None, examples=["Encuentro"])

    @model_validator(mode="before")
    @classmethod
    def check_at_least_one_field(cls, data):
        if isinstance(data, dict) and not data:
            raise ValueError("Debe enviar al menos un campo para actualizar")
        return data
