from __future__ import annotations
from app.contrib import ModelBase
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.modules.category import CategoryModel
    from app.modules.training_center import TrainingCenterModel




__all__ = ["AthleteModel"]


class AthleteModel(ModelBase):
    __tablename__ = "athletes"
    pk_id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    document_number: Mapped[str] = mapped_column(sa.String(11), unique=True, nullable=False)
    age: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    weight: Mapped[float] = mapped_column(sa.Float, nullable=False)
    height: Mapped[float] = mapped_column(sa.Float, nullable=False)
    gender: Mapped[str] = mapped_column(sa.String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, default=sa.func.now())
    category_id: Mapped[int] = mapped_column(sa.ForeignKey("categories.pk_id"))
    category: Mapped["CategoryModel"] = relationship(back_populates="athlete", lazy="selectin")
    training_center_id: Mapped[int] = mapped_column(sa.ForeignKey("training_centers.pk_id"))
    training_center: Mapped["TrainingCenterModel"] = relationship(back_populates="athlete", lazy="selectin")