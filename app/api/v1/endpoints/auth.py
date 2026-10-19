# app/api/v1/endpoints/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service
from app.core.security import create_access_token

# --- NUEVAS IMPORTACIONES PARA LA RUTA PROTEGIDA ---
from app.dependencies.deps import get_current_user
from app.models.user import User

# APIRouter es como un "mini FastAPI" para agrupar rutas
router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Registra un nuevo hincha en la base de datos.
    """
    user_exists = await user_service.get_user_by_email(db, email=user_in.email)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado. ¡Ya sos socio del Ciclón!"
        )
    
    new_user = await user_service.create_user(db, user_in)
    return new_user

@router.post("/login")
async def login(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Inicia sesión y devuelve un Token JWT.
    """
    user = await user_service.authenticate_user(db, email=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.id)
    
    return {"access_token": access_token, "token_type": "bearer"}

# --- NUEVA RUTA PROTEGIDA ---
@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Devuelve el perfil del usuario actual.
    Para acceder, el frontend debe enviar el Token JWT en el header.
    """
    return current_user