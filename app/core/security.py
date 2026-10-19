# app/core/security.py
from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings
from typing import Any
from passlib.context import CryptContext

# Configuramos el contexto de encriptación.
# "bcrypt" es el algoritmo, "deprecated=auto" permite actualizar a algoritmos más nuevos en el futuro.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compara una contraseña en texto plano con un hash guardado en la base de datos.
    Retorna True si coinciden, False si no.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Toma una contraseña en texto plano y devuelve su versión encriptada (hash).
    """
    return pwd_context.hash(password)

def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    """
    Crea un token JWT firmado.
    'subject' suele ser el ID del usuario o su email.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # El payload es la información que viaja dentro del token. 
    # 'exp' es la fecha de expiración y 'sub' es el sujeto (usuario).
    to_encode = {"exp": expire, "sub": str(subject)}
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> str | None:
    """
    Verifica si un token es válido y no ha expirado.
    Si es válido, devuelve el 'subject' (ID del usuario). Si no, devuelve None.
    """
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded_token.get("sub")
    except jwt.PyJWTError:
        # Si el token está vencido o fue manipulado, PyJWT lanza un error que atrapamos acá.
        return None