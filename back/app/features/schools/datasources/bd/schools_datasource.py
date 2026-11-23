
from sqlalchemy.orm import Session

from app.features.schools.models.schools_models import SchoolModel

class SchoolsDatasource:
    """
    Clase que representa la fuente de datos para las escuelas.
    """

    def __init__(self, db_connection:Session):
        """
        Inicializo la fuente de datos.
        """
        self.db_connection = db_connection
        

    def get_schools(self, school_name: str | None = None, limit: int = 20, offset: int = 0) -> list[SchoolModel]:
        """
        Obtiene una o más escuelas según el nombre.

        :param school_name: Nombre de la escuela a buscar.
        :param limit: Número máximo de resultados a devolver.
        :param offset: Número de resultados a omitir.
        :return: Lista de escuelas que coinciden con el criterio de búsqueda.
        """
        
        query = self.db_connection.query(SchoolModel)
        
        if school_name:
            query = query.filter(SchoolModel.name.ilike(f"%{school_name}%"))
        
        return query.limit(limit).offset(offset).all()