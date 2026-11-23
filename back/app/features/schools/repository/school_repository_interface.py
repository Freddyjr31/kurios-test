
from abc import ABC, abstractmethod

class SchoolsRepositoryInterface(ABC):
    """
    Interfaz para el repositorio de escuelas.
    Define los métodos que deben implementarse en cualquier clase que actúe como repositorio de escuelas.
    """

    @abstractmethod
    def get_schools(
        self,
         *,
        name: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ):
        """
        Obtiene todas las escuelas.
        adicionalmente, permite filtrar por nombre y paginar los resultados.
        """
        pass
    