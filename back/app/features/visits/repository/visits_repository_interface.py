from abc import ABC, abstractmethod
from datetime import date, time

from app.features.visits.models.visits_models import SchoolVisitModel, VisitWithNames


class VisitsRepositoryInterface(ABC):
    """
    Interfaz para el repositorio de visitas.
    Define los métodos que debe implementar cualquier repositorio de visitas.
    """

    @abstractmethod
    def get_type_visits(self) -> list[str]:
        """
        Obtiene los tipos de visita definidos en el enum `type_visits_enum`.

        :return: Valores del enum en el orden definido en la base de datos.
        """

    @abstractmethod
    def get_visits(
        self,
        *,
        school_id: int | None = None,
        type_visit: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[VisitWithNames]:
        """
        Obtiene las visitas visibles con los nombres de colegio y profesor.

        :param school_id: ID del colegio.
        :param type_visit: Tipo de visita.
        :param limit: Número máximo de resultados a devolver.
        :param offset: Número de resultados a omitir.
        """

    @abstractmethod
    def count_visits(
        self,
        *,
        school_id: int | None = None,
        type_visit: str | None = None,
    ) -> int:
        """
        Cuenta las visitas visibles que cumplen los filtros.
        """

    @abstractmethod
    def get_visit(self, visit_id: int) -> SchoolVisitModel | None:
        """
        Obtiene una visita por ID, sin importar su estado.
        """

    @abstractmethod
    def school_exists(self, school_id: int) -> bool:
        """
        Indica si el colegio existe.
        """

    @abstractmethod
    def get_teacher_school(self, teacher_id: int) -> int | None:
        """
        Devuelve el colegio del profesor, o None si no existe.
        """

    @abstractmethod
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
        """

    @abstractmethod
    def create_visit(self, visit: SchoolVisitModel) -> SchoolVisitModel:
        """
        Crea una nueva visita.

        :param visit: Objeto `SchoolVisitModel` con los datos de la visita.
        :return: La visita creada con su ID asignado.
        """

    @abstractmethod
    def update_visit(
        self, visit_id: int, updated_data: dict
    ) -> SchoolVisitModel | None:
        """
        Actualiza los campos editables de una visita existente.

        :param visit_id: ID de la visita a actualizar.
        :param updated_data: Campos a actualizar y sus nuevos valores.
        :return: La visita actualizada, o None si no existe.
        """

    @abstractmethod
    def soft_delete_visit(self, visit_id: int) -> bool:
        """
        Oculta una visita cambiando su estado a `hide`.

        :param visit_id: ID de la visita a ocultar.
        :return: True si la visita existe (aunque ya estuviera oculta),
                 False si no existe.
        """
