# app/dependencies/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.core.security import decode_access_token
from app.models.user import User

# Esta línea le dice a FastAPI que busque el token en el header "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependencia que valida el token JWT y devuelve el usuario actual.
    Si el token es inválido o expiró, lanza un error 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Decodificamos el token
    user_id_str = decode_access_token(token)
    if user_id_str is None:
        raise credentials_exception

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise credentials_exception

    # 2. Buscamos al usuario en la base de datos
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Verifica que el usuario autenticado sea superusuario.
    Si no lo es, lanza un 403 (autenticado pero sin permisos).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tenés permisos de administrador para esta acción.",
        )
    return current_user