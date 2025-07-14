from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime


__all__ = ["SchemaBase", "SchemaBaseOutput"]


class SchemaBase(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class SchemaBaseOutput(SchemaBase):
    id: UUID = Field(title="ID", description="ID do registro")
    created_at: datetime = Field(title="Data de criação", description="Data de criação do registro")