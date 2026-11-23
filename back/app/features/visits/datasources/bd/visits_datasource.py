from datetime import date, time

from sqlalchemy import func, text
from sqlalchemy.orm import Query, Session

from app.features.schools.models.schools_models import SchoolModel
from app.features.teachers.models.teachers_models import TeacherModel
from app.features.visits.enums import VisitStatusEnum
from app.features.visits.models.visits_models import SchoolVisitModel, VisitWithNames

TYPE_VISITS_ENUM_NAME = "type_visits_enum"
VISIBLE = VisitStatusEnum.VISIBLE.value

#: Campos que un cliente puede modificar. `id`, `visit_status` y `created_at`
#: nunca se actualizan desde un body.
EDITABLE_FIELDS = frozenset(
    {"id_school", "id_teacher", "date_visit", "time_visit", "notes", "type_visit"}
)


class VisitsDatasource:
    """
    Clase que representa la fuente de datos para las visitas.
    """

    def __init__(self, db_connection: Session):
        """
        Inicializo la fuente de datos.
        """
        self.db_connection = db_connection

    # ------------------------------------------------------------------
    # Catálogos y validaciones
    # ------------------------------------------------------------------

    def get_type_visits(self) -> list[str]:
        """
        Lee los valores del enum `type_visits_enum` directamente desde
        `pg_enum`, respetando el orden definido en la base de datos.

        :return: Lista de tipos de visitas disponibles.
        """
        query = text(
            """
            SELECT e.enumlabel
            FROM pg_enum AS e
            JOIN pg_type AS t ON e.enumtypid = t.oid
            JOIN pg_namespace AS n ON t.typnamespace = n.oid
            WHERE t.typname = :enum_name
              AND n.nspname = 'public'
            ORDER BY e.enumsortorder
            """
        )
        rows = self.db_connection.execute(
            query, {"enum_name": TYPE_VISITS_ENUM_NAME}
        )
        return [row[0] for row in rows]

    def school_exists(self, school_id: int) -> bool:
        """
        Indica si el colegio existe.
        """
        return (
            self.db_connection.query(SchoolModel.id)
            .filter(SchoolModel.id == school_id)
            .first()
            is not None
        )

    def get_teacher_school(self, teacher_id: int) -> int | None:
        """
        Devuelve el colegio al que pertenece el profesor.

        :return: ID del colegio, o None si el profesor no existe.
        """
        row = (
            self.db_connection.query(TeacherModel.id_school)
            .filter(TeacherModel.id == teacher_id)
            .first()
        )
        return row[0] if row is not None else None

    # ------------------------------------------------------------------
    # Lecturas
    # ------------------------------------------------------------------

    def _base_query(
        self,
        school_id: int | None = None,
        type_visit: str | None = None,
    ) -> Query:
        """
        Consulta base: solo visitas visibles y los filtros opcionales.
        """
        query = self.db_connection.query(SchoolVisitModel).filter(
            SchoolVisitModel.visit_status == VISIBLE
        )

        if school_id is not None:
            query = query.filter(SchoolVisitModel.id_school == school_id)
        if type_visit is not None:
            query = query.filter(SchoolVisitModel.type_visit == type_visit)

        return query

    def get_visits(
        self,
        *,
        school_id: int | None = None,
        type_visit: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[VisitWithNames]:
        """
        Obtiene las visitas visibles junto con el nombre del colegio y del
        profesor, ordenadas de la más reciente a la más antigua.

        :param school_id: ID del colegio.
        :param type_visit: Tipo de visita.
        :param limit: Número máximo de resultados a devolver.
        :param offset: Número de resultados a omitir.
        :return: Lista de visitas con sus nombres resueltos.
        """
        query = (
            self.db_connection.query(
                SchoolVisitModel,
                SchoolModel.name.label("school_name"),
                func.concat_ws(
                    " ", TeacherModel.name, TeacherModel.last_name
                ).label("teacher_name"),
            )
            .outerjoin(SchoolModel, SchoolModel.id == SchoolVisitModel.id_school)
            .outerjoin(
                TeacherModel, TeacherModel.id == SchoolVisitModel.id_teacher
            )
            .filter(SchoolVisitModel.visit_status == VISIBLE)
        )

        if school_id is not None:
            query = query.filter(SchoolVisitModel.id_school == school_id)
        if type_visit is not None:
            query = query.filter(SchoolVisitModel.type_visit == type_visit)

        rows = (
            query.order_by(
                SchoolVisitModel.date_visit.desc().nulls_last(),
                SchoolVisitModel.time_visit.desc().nulls_last(),
                SchoolVisitModel.id.desc(),
            )
            .limit(limit)
            .offset(offset)
            .all()
        )

        return [
            VisitWithNames(
                visit=visit,
                school_name=school_name,
                # concat_ws devuelve '' cuando todos los argumentos son NULL
                teacher_name=teacher_name or None,
            )
            for visit, school_name, teacher_name in rows
        ]

    def count_visits(
        self,
        *,
        school_id: int | None = None,
        type_visit: str | None = None,
    ) -> int:
        """
        Cuenta las visitas visibles que cumplen los filtros.
        """
        return self._base_query(school_id, type_visit).count()

    def get_visit(self, visit_id: int) -> SchoolVisitModel | None:
        """
        Obtiene una visita por ID, sin importar su estado.
        """
        return self.db_connection.get(SchoolVisitModel, visit_id)

    def exists_visit_at(
        self,
        *,
        teacher_id: int,
        date_visit: date,
        time_visit: time,
        exclude_visit_id: int | None = None,
    ) -> bool:
        """
        Indica si el profesor ya tiene una visita visible en esa fecha y hora.

        :param exclude_visit_id: Visita a excluir (para ediciones).
        """
        query = self.db_connection.query(SchoolVisitModel.id).filter(
            SchoolVisitModel.visit_status == VISIBLE,
            SchoolVisitModel.id_teacher == teacher_id,
            SchoolVisitModel.date_visit == date_visit,
            SchoolVisitModel.time_visit == time_visit,
        )

        if exclude_visit_id is not None:
            query = query.filter(SchoolVisitModel.id != exclude_visit_id)

        return query.first() is not None

    # ------------------------------------------------------------------
    # Escrituras
    # ------------------------------------------------------------------

    def create_visit(self, visit: SchoolVisitModel) -> SchoolVisitModel:
        """
        Crea una nueva visita en la base de datos.

        :param visit: Objeto `SchoolVisitModel` con los datos de la visita.
        :return: La visita creada con su ID asignado.
        """
        self.db_connection.add(visit)
        self.db_connection.commit()
        self.db_connection.refresh(visit)
        return visit

    def update_visit(
        self, visit_id: int, updated_data: dict
    ) -> SchoolVisitModel | None:
        """
        Actualiza una visita existente. Solo aplica los campos editables.

        :param visit_id: ID de la visita a actualizar.
        :param updated_data: Campos a actualizar y sus nuevos valores.
        :return: La visita actualizada, o None si no existe.
        """
        visit = self.db_connection.get(SchoolVisitModel, visit_id)

        if visit is None:
            return None

        for key, value in updated_data.items():
            if key in EDITABLE_FIELDS:
                setattr(visit, key, value)

        self.db_connection.commit()
        self.db_connection.refresh(visit)
        return visit

    def soft_delete_visit(self, visit_id: int) -> bool:
        """
        Oculta una visita cambiando `visit_status` a `hide`.

        No elimina el registro: la visita queda como transacción histórica.

        :param visit_id: ID de la visita a ocultar.
        :return: True si la visita existe, False si no existe.
        """
        visit = self.db_connection.get(SchoolVisitModel, visit_id)

        if visit is None:
            return False

        if visit.visit_status != VisitStatusEnum.HIDE.value:
            visit.visit_status = VisitStatusEnum.HIDE.value
            self.db_connection.commit()
            self.db_connection.refresh(visit)

        return True
