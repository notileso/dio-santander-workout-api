from app.core.repository import RepositoryBase, AsyncSessionCallable
from .models import TrainingCenterModel
from .schemas import *

__all__ = [
    "TrainingCenterRepository"
]

class TrainingCenterRepository(RepositoryBase[TrainingCenterModel, TrainingCenterInput, TrainingCenterOutput, TrainingCenterFilter]):
    def __init__(self, *,session_callable: AsyncSessionCallable | None = None):
        super().__init__(TrainingCenterModel, TrainingCenterInput, TrainingCenterOutput, TrainingCenterFilter, session_callable=session_callable)
