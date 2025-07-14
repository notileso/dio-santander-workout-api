from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession

from app.contrib.dependencies import *
from app.modules.training_center import *
from app.modules.category import *
from typing import Annotated
from .schemas import *
from .models import *
from .repository import *
from app.core.databases import get_async_session
from app.core.repository import Page



__all__ = ["router"]


router = APIRouter()


async def _get_athlete(
    athlete_id: UUID,
    athlete_repository: AthleteRepositoryDependency = Depends(),
):
    """
    Retorna um atleta pelo ID
    """
    athlete_filter = AthleteFilter(id=athlete_id)
    db_athlete = await athlete_repository.find_one(filter_in=athlete_filter)
    if db_athlete is None:
        raise HTTPException(status_code=404, detail="Não foi possível encontrar o atleta")
    return db_athlete


@router.get("/", response_model=Page[AthleteOutput])
async def get_all_athletes_router(*,
    athlete_filter: Annotated[AthleteFilter, Query()],
    athlete_repository: AthleteRepositoryDependency,
):
    """
    Retorna todos os Atletas
    """
    db_athletes = await athlete_repository.paginate(filter_in=athlete_filter,page=athlete_filter.page, size=athlete_filter.size)
    return db_athletes


@router.post("/", response_model=AthleteOutput)
async def create_athlete_router(
    athlete: AthleteInput,
    athlete_repository: AthleteRepositoryDependency,
    training_center_repository: TrainingCenterRepositoryDependency,
    category_repository: CategoryRepositoryDependency,
    async_session: AsyncSession = Depends(get_async_session),
):
    """
    Cria uma nova categoria
    """
    db_category = await category_repository.find_one(
        filter_in=CategoryFilter(id=[athlete.category_id]),
        async_session=async_session,
    )
    if db_category is None:
        raise HTTPException(status_code=404, detail="Não foi possível encontrar a categoria")
    db_training_center = await training_center_repository.find_one(
        filter_in=TrainingCenterFilter(id=athlete.training_center_id),
        async_session=async_session,
    )
    if db_training_center is None:
        raise HTTPException(status_code=404, detail="Não foi possível encontrar o centro de treinamento")
    db_athlete = AthleteModel(
        **athlete.model_dump(exclude={"category_id", "training_center_id"}),
        training_center_id=db_training_center.pk_id,
        category_id=db_category.pk_id,
    )
    try:
        db_athlete = await athlete_repository.create(obj_in=db_athlete, async_session=async_session)
        db_athlete.training_center = db_training_center
        db_athlete.category = db_category
    except exc.IntegrityError as e:
        raise HTTPException(status_code=303, detail=f"Já existe cpf cadastrado com esse número {db_athlete.document_number}") from e
    return db_athlete


@router.get("/{athlete_id}", response_model=AthleteOutput)
async def get_athlete_router(athlete_id: UUID):
    """
    Retorna uma categoria pelo ID
    """
    return await _get_athlete(athlete_id)


@router.patch("/{athlete_id}", response_model=AthleteOutput)
async def update_athlete_router(
    athlete_id: UUID,
    athlete: AthleteUpdate,
    athlete_repository: AthleteRepositoryDependency,
):
    """
    Atualiza uma categoria pelo ID
    """

    db_athlete = await athlete_repository.update(id=athlete_id, obj_in=athlete)
    return db_athlete


@router.delete("/{athlete_id}", status_code=204)
async def delete_athlete_router(
    athlete_id: UUID,
    athlete_repository: AthleteRepositoryDependency,
):
    """
    Deleta uma categoria pelo ID
    """
    db_athlete = await athlete_repository.remove(id=athlete_id)
    if db_athlete is None:
        raise HTTPException(status_code=404, detail="Não foi possível encontrar o atleta")
    return
