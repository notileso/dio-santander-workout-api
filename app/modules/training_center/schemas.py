from app.contrib import SchemaBase, SchemaBaseOutput
from pydantic import Field
from uuid import UUID

__all__ = ["TrainingCenterInput", "TrainingCenterOutput", "TrainingCenterFilter", "ListTrainingCenterOutput"]


class TrainingCenterBase(SchemaBase):
    name: str = Field(title="Nome", description="Nome da centro de treinamento", max_length=20, examples=["CT King"])
    address: str = Field(title="Endereço", description="Endereço do centro de treinamento", max_length=50, examples=["Rua das Flores, 123"])
    owner: str = Field(title="Dono", description="Dono do centro de treinamento", max_length=50, examples=["João da Silva"])


class TrainingCenterInput(TrainingCenterBase):
    pass

class TrainingCenterOutput(TrainingCenterBase, SchemaBaseOutput):
    pass

class TrainingCenterFilter(SchemaBase):
    id: UUID | None = None
    name: str | None = None
    address: str | None = None
    owner: str | None = None

ListTrainingCenterOutput = list[TrainingCenterOutput]