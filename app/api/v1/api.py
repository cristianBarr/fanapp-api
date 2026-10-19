# app/api/v1/api.py

from fastapi import APIRouter
from app.api.v1.endpoints import auth

api_router = APIRouter()

# Incluimos las rutas de auth bajo el prefijo /auth
# (y a futuro agregaremos users, matches, posts, etc.)
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])