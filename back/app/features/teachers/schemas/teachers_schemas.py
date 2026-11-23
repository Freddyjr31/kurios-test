from pydantic import BaseModel, ConfigDict, Field


class TeacherBaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., examples=[1])
    name: str | None = Field(..., examples=["Ana"])
    last_name: str | None = Field(..., examples=["Pérez"])
    id_school: int = Field(..., examples=[1])


class TeachersResponse(BaseModel):
    teachers: list[TeacherBaseResponse] = Field(
        ...,
        examples=[[{"id": 1, "name": "Ana", "last_name": "Pérez", "id_school": 1}]],
    )
    total: int = Field(..., examples=[2])
    limit: int = Field(..., examples=[20])
    offset: int = Field(..., examples=[0])
