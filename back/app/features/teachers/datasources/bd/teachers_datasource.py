from sqlalchemy import func, or_
from sqlalchemy.orm import Query, Session

from app.features.teachers.models.teachers_models import TeacherModel


class TeachersDatasource:
    """
    Clase que representa la fuente de datos para los maestros.
    """

    def __init__(self, db_connection: Session):
        """
        Inicializo la fuente de datos.
        """
        self.db_connection = db_connection

    @staticmethod
    def _like_pattern(term: str) -> str:
        """
        Escapa los comodines de SQL (%, _ y \\) para que el término se busque literal.
        """
        escaped = (
            term.replace("\\", "\\\\")
            .replace("%", "\\%")
            .replace("_", "\\_")
        )
        return f"%{escaped}%"

    def _build_query(self, school_id: int, name: str | None) -> Query:
        """
        Arma la consulta base: siempre filtra por colegio y opcionalmente por nombre.

        La búsqueda usa `unaccent` para que "perez" encuentre "Pérez" y
        "jose" encuentre "José", sin distinguir mayúsculas.
        """
        query = self.db_connection.query(TeacherModel).filter(
            TeacherModel.id_school == school_id
        )

        if name:
            pattern = func.unaccent(self._like_pattern(name))
            full_name = func.unaccent(
                func.concat_ws(" ", TeacherModel.name, TeacherModel.last_name)
            )
            query = query.filter(
                or_(
                    func.unaccent(TeacherModel.name).ilike(pattern, escape="\\"),
                    func.unaccent(TeacherModel.last_name).ilike(pattern, escape="\\"),
                    full_name.ilike(pattern, escape="\\"),
                )
            )

        return query

    def get_teachers(
        self,
        *,
        school_id: int,
        name: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[TeacherModel]:
        """
        Obtiene los maestros de un colegio.

        :param school_id: Colegio al que pertenecen los maestros.
        :param name: Texto a buscar en el nombre, apellido o nombre completo.
        :param limit: Número máximo de resultados a devolver.
        :param offset: Número de resultados a omitir.
        :return: Lista de maestros que coinciden con el criterio de búsqueda.
        """
        return (
            self._build_query(school_id, name)
            .order_by(TeacherModel.last_name, TeacherModel.name)
            .limit(limit)
            .offset(offset)
            .all()
        )

    def count_teachers(self, *, school_id: int, name: str | None = None) -> int:
        """
        Cuenta los maestros de un colegio que coinciden con el filtro.

        :param school_id: Colegio al que pertenecen los maestros.
        :param name: Texto a buscar en el nombre, apellido o nombre completo.
        :return: Total de maestros que cumplen el criterio.
        """
        return self._build_query(school_id, name).count()
