# app/schemas/match.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.schemas.team import TeamMini


# 1. Esquema Base: Propiedades compartidas entre creación y respuesta
class MatchBase(BaseModel):
    match_date: datetime
    stadium: str = Field(..., min_length=1, max_length=255)
    home_score: int = Field(0, ge=0)
    away_score: int = Field(0, ge=0)
    status: str = Field("scheduled", max_length=20)
    competition: Optional[str] = Field(None, max_length=100)


# 2. Crear un partido: requiere los IDs de los equipos
class MatchCreate(MatchBase):
    home_team_id: int = Field(..., gt=0)
    away_team_id: int = Field(..., gt=0)


# 3. Actualizar un partido: todos los campos opcionales (semántica PATCH)
class MatchUpdate(BaseModel):
    match_date: Optional[datetime] = None
    stadium: Optional[str] = Field(None, min_length=1, max_length=255)
    home_score: Optional[int] = Field(None, ge=0)
    away_score: Optional[int] = Field(None, ge=0)
    status: Optional[str] = Field(None, max_length=20)
    competition: Optional[str] = Field(None, max_length=100)


# 4. Respuesta: IDs + objetos anidados (Opción C híbrida)
class MatchResponse(MatchBase):
    id: int
    home_team_id: int
    away_team_id: int
    home_team: Optional[TeamMini] = None
    away_team: Optional[TeamMini] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}