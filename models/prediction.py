from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from core.database import Base

if TYPE_CHECKING:
    from models.user import User

class Prediction(Base):

    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    title: Mapped[str] = mapped_column(
        String(200)
    )

    text: Mapped[str] = mapped_column(
        String(5000)
    )

    prediction: Mapped[str] = mapped_column(
        String(10)
    )

    probability: Mapped[float] = mapped_column(
        Float
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    note: Mapped[str | None] = mapped_column(
        String(150),
        default=None
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="predictions")

    