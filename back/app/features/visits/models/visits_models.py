from dataclasses import dataclass
from datetime import date, datetime, time

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    ForeignKey,
    Identity,
    String,
    Time,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SchoolVisitModel(Base):
    """
    Visita realizada a un colegio.

    Refleja el esquema real de la tabla `school_visits` en PostgreSQL.
    
    `visit_status` y `type_visit` son enums nativos de la base
    (`visit_status_enum` y `type_visits_enum`); se mapean como texto para que
    la app no falle si se agregan valores nuevos al enum desde Supabase.
    """

    __tablename__ = "school_visits"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    id_school: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("schools.id"), nullable=True
    )
    id_teacher: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("teachers.id"), nullable=True
    )
    date_visit: Mapped[date | None] = mapped_column(Date, nullable=True)
    time_visit: Mapped[time | None] = mapped_column(Time, nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=func.now()
    )
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    visit_status: Mapped[str | None] = mapped_column(String, nullable=True)
    type_visit: Mapped[str | None] = mapped_column(String, nullable=True)


@dataclass
class VisitWithNames:
    """
    Resultado del listado: la visita y los nombres resueltos por JOIN.
    """

    visit: SchoolVisitModel
    school_name: str | None
    teacher_name: str | None
