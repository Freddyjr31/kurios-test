

from pydantic import BaseModel, ConfigDict, Field

class SchoolBaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Springfield Elementary"])
    address: str = Field(..., examples=["742 Evergreen Terrace, Springfield"])
    
class SchoolsResponse(BaseModel):
    schools: list[SchoolBaseResponse] = Field(..., examples=[[{"id": 1, "name": "U.E Maria Auxiliadora", "address": "El Rosal, Caracas"}]])
    total: int = Field(..., examples=[2])
    limit: int = Field(..., examples=[20])
    offset: int = Field(..., examples=[0])