from fastapi import APIRouter, HTTPException, Query
from .schemas import *
from .repository import *
from .models import *
from app.core.databases import get_async_context_session
from uuid import UUID
from typing import Annotated



__all__ = ["router"]

training_center_repository = TrainingCenterRepository(session_callable=get_async_context_session)

router = APIRouter()


@router.get("/", response_model=ListTrainingCenterOutput)
async def get_all_training_centers_router(filter_in: Annotated[TrainingCenterFilter, Query()]):
    """
    Retorna todos os Centros de Treinamento.
    """
    db_training_centers = await training_center_repository.find_all(filter_in=filter_in)
    return db_training_centers


@router.post("/", response_model=TrainingCenterOutput)
async def create_training_center_router(
    training_center: TrainingCenterInput,
):
    """
    Cria um novo Centro de Treinamento.
    """

    db_training_center = training_center_repository.create(obj_in=training_center)
    return db_training_center


@router.get("/{training_center_id}", response_model=TrainingCenterOutput)
async def get_training_center_router(
    training_center_id: UUID,
):
    """
    Retorna um centro de Treinamento pelo ID
    """
    db_training_center = await training_center_repository.find_one(
        filter_in=TrainingCenterFilter(id=training_center_id)
    )
    if db_training_center is None:
        raise HTTPException(404, detail="Training Center not found")
    return db_training_center
