from fastapi import APIRouter, HTTPException, Query
from .schemas import ListCategoryOutput, CategoryOutput, CategoryInput, CategoryFilter
from .repository import CategoryRepository
from sqlalchemy import exc
from uuid import UUID
from typing import Annotated
from app.core.databases import get_async_context_session

__all__ = ["router"]

category_repository = CategoryRepository(session_callable=get_async_context_session)


router = APIRouter()


@router.get("/", response_model=ListCategoryOutput)
async def get_all_athletes_router(filter_input: Annotated[CategoryFilter, Query()]):
    """
    Retorna todos as categorias
    """

    db_categories = await category_repository.find_all(filter_in=filter_input)
    return db_categories

@router.post("/", response_model=CategoryOutput)
async def create_category_router(category: CategoryInput):
    """
    Cria uma nova categoria
    """
    try:
        db_category = await category_repository.create(obj_in=category)
    except exc.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Não foi possível criar a categoria") from e
    return db_category


@router.get("/{category_id}", response_model=CategoryOutput)
async def get_category_router(category_id: UUID):
    """
    Retorna uma categoria pelo ID
    """
    category_filter = CategoryFilter(id=[category_id])
    db_category = await category_repository.find_one(filter_in=category_filter)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Não foi possível encontrar a categoria")
    return db_category