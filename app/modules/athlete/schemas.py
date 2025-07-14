from uuid import UUID
from pydantic import Field
from typing import Literal
from app.modules.category import CategoryOutput
from app.contrib import SchemaBase
from app.modules.training_center import TrainingCenterOutput

__all__ = ["AthleteInput", "AthleteOutput", "AthleteUpdate", "AthleteFilter", "ListAthleteOutput"]


class AthleteBase(SchemaBase):
    name: str = Field(
        title="Nome",
        description="Nome do Atleta",
        max_length=50,
        examples=["João de Oliveira", "Maria Silva", "José Santos"],
    )
    document_number: str = Field(
        title="CPF",
        description="CPF do Atleta",
        max_length=11,
        pattern=r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$",
        examples=["12345678901", "123.456.789-01"],
    )
    age: int = Field(
        title="Idade", description="Idade do Atleta", ge=1, le=99, examples=[25, 30, 35]
    )
    weight: float = Field(
        title="Peso", description="Peso do Atleta", ge=1, le=400, examples=[60, 65, 70]
    )
    height: float = Field(
        title="Altura",
        description="Altura do Atleta",
        ge=1,
        le=3,
        examples=[1.70, 1.75, 1.80],
    )
    gender: Literal["M", "F"] = Field(title="Sexo", description="Sexo do Atleta")

class AthleteInput(AthleteBase):
    category_id: UUID = Field(title="ID da Categoria")
    training_center_id: UUID = Field(title="ID do Centro de Treinamento")

class AthleteOutput(SchemaBase):
    name: str
    category: CategoryOutput
    training_center: TrainingCenterOutput

class AthleteUpdate(SchemaBase):
    name: str | None = None
    weight: int | None = None
    height: float | None = None
    age: int | None = None
    
class AthleteFilter(SchemaBase):
    id: UUID | None = None
    document_number: str | None = None
    name: str | None = None
    age: int | None = None
    weight: int | None = None
    height: float | None = None
    gender: str | None = None
    page: int = Field(default=1, exclude=True)
    size: int = Field(default=20, exclude=True)


ListAthleteOutput = list[AthleteOutput]