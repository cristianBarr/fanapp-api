# app/schemas/team.py
from pydantic import BaseModel
from typing import Optional


class TeamMini(BaseModel):
    id: int
    name: str
    short_name: Optional[str] = None
    logo_url: Optional[str] = None

    model_config = {"from_attributes": True}