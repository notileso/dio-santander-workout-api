from __future__ import annotations
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING
from app.contrib import ModelBase
if TYPE_CHECKING:
    from app.modules.athlete import AthleteModel


__all__ = ["TrainingCenterModel"]


class TrainingCenterModel(ModelBase):
    __tablename__ = "training_centers"
    pk_id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(20), nullable=False)
    address: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    owner: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, default=sa.func.now())
    athlete: Mapped["AthleteModel"] = relationship(back_populates="training_center")