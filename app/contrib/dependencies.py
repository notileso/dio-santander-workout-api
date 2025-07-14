from typing import Annotated
from fastapi import Depends
from app.core.databases import get_async_context_session
from app.modules.athlete.repository import AthleteRepository
from app.modules.category.repository import CategoryRepository
from app.modules.training_center.repository import TrainingCenterRepository
from app.modules.athlete import AthleteModel
from app.modules.category import CategoryModel
from app.modules.training_center import TrainingCenterModel

__all__ = [
    "AthleteModel",
    "CategoryModel",
    "TrainingCenterModel",
    "AthleteRepositoryDependency",
    "CategoryRepositoryDependency",
    "TrainingCenterRepositoryDependency",
]


def _get_athlete_repository() -> AthleteRepository:
    return AthleteRepository(session_callable=get_async_context_session)


def _get_category_repository() -> CategoryRepository:
    return CategoryRepository(session_callable=get_async_context_session)


def _get_training_center_repository() -> TrainingCenterRepository:
    return TrainingCenterRepository(session_callable=get_async_context_session)

AthleteRepositoryDependency = Annotated[AthleteRepository, Depends(_get_athlete_repository)]
CategoryRepositoryDependency = Annotated[CategoryRepository, Depends(_get_category_repository)]
TrainingCenterRepositoryDependency = Annotated[TrainingCenterRepository, Depends(_get_training_center_repository)]