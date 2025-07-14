from __future__ import annotations
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.contrib import ModelBase
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.athlete import AthleteModel


__all__ = ["CategoryModel"]


class CategoryModel(ModelBase):
    __tablename__ = "categories"
    pk_id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(20), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, default=sa.func.now())
    athlete: Mapped["AthleteModel"] = relationship(back_populates="category")