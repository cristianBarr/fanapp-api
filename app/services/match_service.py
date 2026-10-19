# app/services/match_service.py
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.match import Match
from app.models.team import Team
from app.schemas.match import MatchCreate, MatchUpdate


# Opciones de carga reutilizables: siempre que leamos un Match,
# cargamos sus equipos con un segundo SELECT (evita lazy="raise").
_MATCH_LOAD_OPTIONS = (
    selectinload(Match.home_team),
    selectinload(Match.away_team),
)


async def get_match(session: AsyncSession, match_id: int) -> Match | None:
    result = await session.execute(
        select(Match)
        .options(*_MATCH_LOAD_OPTIONS)
        .where(Match.id == match_id)
    )
    return result.scalar_one_or_none()


async def list_matches(
    session: AsyncSession,
    *,
    team_id: int | None = None,
    limit: int = 50,
    offset: int = 0,
) -> Sequence[Match]:
    stmt = (
        select(Match)
        .options(*_MATCH_LOAD_OPTIONS)
        .order_by(Match.match_date.desc())
        .limit(limit)
        .offset(offset)
    )
    if team_id is not None:
        stmt = stmt.where(
            (Match.home_team_id == team_id) | (Match.away_team_id == team_id)
        )
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_match(session: AsyncSession, payload: MatchCreate) -> Match:
    if payload.home_team_id == payload.away_team_id:
        raise ValueError("home_team_id y away_team_id deben ser distintos")
    await _ensure_teams_exist(session, payload.home_team_id, payload.away_team_id)

    match = Match(**payload.model_dump())
    session.add(match)
    await session.commit()
    return await get_match(session, match.id)  # type: ignore[return-value]


async def update_match(
    session: AsyncSession, match_id: int, payload: MatchUpdate
) -> Match | None:
    match = await get_match(session, match_id)
    if match is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(match, field, value)

    await session.commit()
    session.expire(match)  # fuerza recarga de updated_at + relaciones
    return await get_match(session, match_id)


async def delete_match(session: AsyncSession, match_id: int) -> bool:
    match = await get_match(session, match_id)
    if match is None:
        return False
    await session.delete(match)
    await session.commit()
    return True


async def _ensure_teams_exist(
    session: AsyncSession, home_team_id: int, away_team_id: int
) -> None:
    """Pre-check de FKs: mejor un ValueError legible que un IntegrityError de Postgres."""
    result = await session.execute(
        select(Team.id).where(Team.id.in_([home_team_id, away_team_id]))
    )
    found = {row[0] for row in result}
    missing = {home_team_id, away_team_id} - found
    if missing:
        raise ValueError(f"Equipos inexistentes: {sorted(missing)}")