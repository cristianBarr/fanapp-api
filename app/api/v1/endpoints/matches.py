# app/api/v1/endpoints/matches.py

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.deps import get_current_active_superuser
from app.models.user import User
from app.schemas.match import MatchCreate, MatchUpdate, MatchResponse
from app.services import match_service

router = APIRouter()


@router.post("/", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
async def create_match(
    payload: MatchCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_active_superuser),
):
    """
    Crea un nuevo partido. **Solo superusuarios.**
    """
    try:
        return await match_service.create_match(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get("/", response_model=list[MatchResponse])
async def list_matches(
    team_id: Optional[int] = Query(
        None, gt=0, description="Filtrar por equipo (local o visitante)"
    ),
    limit: int = Query(50, ge=1, le=200, description="Cantidad máxima de resultados"),
    offset: int = Query(0, ge=0, description="Resultados a saltear (paginación)"),
    db: AsyncSession = Depends(get_db),
):
    """
    Lista partidos ordenados por fecha descendente. **Público.**
    """
    return await match_service.list_matches(
        db, team_id=team_id, limit=limit, offset=offset
    )


@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(
    match_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Obtiene un partido por ID. **Público.**
    """
    match = await match_service.get_match(db, match_id)
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Partido {match_id} no encontrado.",
        )
    return match


@router.patch("/{match_id}", response_model=MatchResponse)
async def update_match(
    match_id: int,
    payload: MatchUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_active_superuser),
):
    """
    Actualiza un partido (parcial). **Solo superusuarios.**
    """
    try:
        match = await match_service.update_match(db, match_id, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Partido {match_id} no encontrado.",
        )
    return match


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_match(
    match_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_active_superuser),
):
    """
    Elimina un partido. **Solo superusuarios.**
    """
    deleted = await match_service.delete_match(db, match_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Partido {match_id} no encontrado.",
        )