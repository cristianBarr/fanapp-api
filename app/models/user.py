# app/models/user.py

from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base

class User(Base):
    """
    Modelo de Usuario (Hincha de San Lorenzo).
    Hereda de Base, lo que le dice a SQLAlchemy que esto es una tabla.
    """
    __tablename__ = "users"  # El nombre de la tabla en PostgreSQL

    # mapped_column y Mapped son la forma moderna (SQLAlchemy 2.0) de definir columnas y tipos.
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Usamos func.now() para que PostgreSQL ponga la fecha automáticamente al crear el usuario.
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())