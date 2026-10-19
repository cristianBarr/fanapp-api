# scripts/make_superuser.py
import asyncio
from sqlalchemy import select, update

from app.db.session import AsyncSessionLocal
from app.models.user import User


async def main() -> None:
    email = "admin@fanapp.com"

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if user is None:
            print(f"❌ No existe usuario con email {email}. Registralo primero en /docs.")
            return

        await session.execute(
            update(User).where(User.email == email).values(is_superuser=True)
        )
        await session.commit()
        print(f"✅ {email} ahora es superusuario (id={user.id}).")


if __name__ == "__main__":
    asyncio.run(main())