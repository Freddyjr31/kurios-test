
from app.features.schools.repository.school_repository_interface import SchoolsRepositoryInterface
from app.features.schools.datasources.bd.schools_datasource import SchoolsDatasource


class SchoolsRepositoryImpl(SchoolsRepositoryInterface):
    def __init__(self, datasource: SchoolsDatasource):
        self.datasource = datasource

    def get_schools(
        self,
        *,
        name: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ):
        """
        Obtiene todas las escuelas desde la fuente de datos.

        :return: Lista de todas las escuelas.
        """
        return self.datasource.get_schools(
            school_name=name,
            limit=limit,
            offset=offset
        )