from abc import ABC, abstractmethod

from app.features.teachers.models.teachers_models import TeacherModel


class TeachersRepositoryInterface(ABC):
    """
    Interfaz para el repositorio de maestros.
    Define los métodos que deben implementarse en cualquier clase que actúe como repositorio de maestros.
    """

    @abstractmethod
    def get_teachers(
        self,
        *,
        school_id: int,
        name: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[TeacherModel]:
        """
        Obtiene los maestros de un colegio, opcionalmente filtrados por nombre o apellido.

        :param school_id: Colegio al que pertenecen los maestros (obligatorio).
        :param name: Texto a buscar en el nombre, apellido o nombre completo.
        :param limit: Número máximo de resultados a devolver.
        :param offset: Número de resultados a omitir.
        """

    @abstractmethod
    def count_teachers(self, *, school_id: int, name: str | None = None) -> int:
        """
        Cuenta los maestros que cumplen el filtro, para la paginación.

        :param school_id: Colegio al que pertenecen los maestros (obligatorio).
        :param name: Texto a buscar en el nombre, apellido o nombre completo.
        """
