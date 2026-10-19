# app/models/match.py
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.team import Team


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    home_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"), index=True, nullable=False
    )
    away_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"), index=True, nullable=False
    )

    match_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True, nullable=False
    )

    stadium: Mapped[str] = mapped_column(String(255), nullable=False)

    home_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    away_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    status: Mapped[str] = mapped_column(
        String(20), default="scheduled", nullable=False
    )

    competition: Mapped[str | None] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relaciones ORM (no afectan el schema de DB, no requieren migración)
    home_team: Mapped["Team"] = relationship(
        "Team",
        foreign_keys=[home_team_id],
        lazy="raise",
    )
    away_team: Mapped["Team"] = relationship(
        "Team",
        foreign_keys=[away_team_id],
        lazy="raise",
    )