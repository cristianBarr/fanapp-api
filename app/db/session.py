# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# 1. Construimos la URL de conexión usando las variables de nuestro .env
# Usamos "postgresql+asyncpg" para indicar que queremos la versión asíncrona.
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

# 2. Creamos el "Motor" (Engine). Es el encargado de manejar las conexiones.
engine = create_async_engine(DATABASE_URL, echo=True) 
# (echo=True hace que en la terminal veamos las consultas SQL que se ejecutan, ideal para debuggear).

# 3. Creamos el "Creador de Sesiones". Cada petición HTTP tendrá su propia sesión.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 4. Esta función es una "Dependencia" de FastAPI.
# Le proveerá una sesión de base de datos a nuestros endpoints y la cerrará automáticamente al terminar.
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()