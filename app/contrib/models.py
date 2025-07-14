import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid import UUID, uuid4

__all__ = ["ModelBase"]

class ModelBase(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(sa.UUID(as_uuid=True), default=uuid4(), nullable=False)
    __abstract__ = True