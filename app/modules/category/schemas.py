from app.contrib import SchemaBase, SchemaBaseOutput
from pydantic import Field
from uuid import UUID

__all__ = [
    "CategoryInput",
    "CategoryOutput",
    "CategoryFilter",
    "ListCategoryOutput",
]


class CategoryBase(SchemaBase):
    name: str = Field(
        title="Nome", description="Nome da categoria", max_length=20, examples=["Scale"]
    )


class CategoryInput(CategoryBase):
    pass


class CategoryOutput(CategoryBase, SchemaBaseOutput):
    pass

class CategoryFilter(SchemaBase):
    id: list[UUID] | None = Field(default=None, serialization_alias="id__in")
    name: str | None = Field(default=None)

ListCategoryOutput = list[CategoryOutput]
