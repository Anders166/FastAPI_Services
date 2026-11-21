from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Esquema para registrar o actualizar una persona
class ServiceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    price: int = Field(max_length=50)
    description:  str = Field(min_length=1, max_length=100)


# Esquema para devolver una persona
class ServiceResponse(BaseModel):
    id: int
    name: str
    price: int
    description: str

    model_config = ConfigDict(from_attributes=True)