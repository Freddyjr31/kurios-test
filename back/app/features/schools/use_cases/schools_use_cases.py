
from app.features.schools.schemas.schools_schemas import SchoolBaseResponse, SchoolsResponse
from app.features.schools.repository.school_repository_interface import SchoolsRepositoryInterface


class SchoolsUseCase:
    
    def __init__(self, repository: SchoolsRepositoryInterface):
        self.repository = repository

    def get_all_schools(
        self, 
        name: str | None = None,
        limit: int | None = None,
        offset: int | None = None
        ) -> SchoolsResponse:
    
        name = name.strip() if name else None
        
        schools = self.repository.get_schools(name=name, limit=limit, offset=offset)
        
        return SchoolsResponse(
            schools=[SchoolBaseResponse(id=school.id, name=school.name, address=school.address) for school in schools],
            total=len(schools),
            limit=limit,
            offset=offset
        )