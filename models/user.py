from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime
from core.database import Base

if TYPE_CHECKING:
    from models.prediction import Prediction

class User(Base):

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    username: Mapped[str] = mapped_column(
        String(70), nullable=False, unique=True
    )

    email: Mapped[str]= mapped_column(
        String(100), unique=True, nullable=False
    )

    hashed_password: Mapped[str]= mapped_column(
        String(255), nullable=False
    )

    role: Mapped[str]= mapped_column(
        String(25), default="user"
    )

    is_active: Mapped[bool]= mapped_column(
        Boolean, default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    predictions: Mapped[list["Prediction"]] = relationship(
    back_populates="user"
)