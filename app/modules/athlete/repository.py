from app.core.repository import RepositoryBase, AsyncSessionCallable
from .models import AthleteModel
from .schemas import *

__all__ = [
    "AthleteRepository"
]

class AthleteRepository(RepositoryBase[AthleteModel, AthleteInput, AthleteUpdate, AthleteFilter]):
    def __init__(self, *,session_callable: AsyncSessionCallable | None = None):
        super().__init__(AthleteModel, AthleteInput, AthleteUpdate, AthleteFilter, session_callable=session_callable)
