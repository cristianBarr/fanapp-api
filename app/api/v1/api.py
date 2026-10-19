# app/api/v1/api.py
from fastapi import APIRouter

from app.api.v1.endpoints import auth, matches

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(matches.router, prefix="/matches", tags=["Partidos"])