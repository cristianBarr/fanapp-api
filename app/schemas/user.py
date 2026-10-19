# app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# 1. Esquema Base: Propiedades compartidas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

# 2. Esquema para crear un usuario (Registro)
# Hereda de UserBase y agrega la contraseña en texto plano (que luego encriptaremos).
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="La contraseña debe tener al menos 8 caracteres")

# 3. Esquema para devolver un usuario (Respuesta de la API)
# Hereda de UserBase y agrega los campos generados por la base de datos.
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    # Configuración para que Pydantic pueda leer desde objetos de SQLAlchemy (los modelos)
    model_config = {"from_attributes": True}