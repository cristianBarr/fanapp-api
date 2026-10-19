# app/services/user_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Busca un usuario por su email en la base de datos."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """Crea un nuevo usuario en la base de datos con la contraseña encriptada."""
    # Encriptamos la contraseña antes de guardarla
    hashed_password = get_password_hash(user_in.password)
    
    # Creamos el objeto de SQLAlchemy (el modelo)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user) # Refrescamos para obtener el ID que generó PostgreSQL
    return db_user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    """Verifica si el email existe y si la contraseña es correcta."""
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user