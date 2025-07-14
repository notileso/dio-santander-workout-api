from app.core.repository import RepositoryBase, AsyncSessionCallable
from .models import CategoryModel
from .schemas import *

__all__ = [
    "CategoryRepository"
]

class CategoryRepository(RepositoryBase[CategoryModel, CategoryInput, CategoryOutput, CategoryFilter]):
    def __init__(self, *,session_callable: AsyncSessionCallable | None = None):
        super().__init__(CategoryModel, CategoryInput, CategoryOutput, CategoryFilter, session_callable=session_callable)
