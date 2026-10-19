# scripts/check_db.py
import asyncio
from sqlalchemy import text
from app.db.session import AsyncSessionLocal


async def main() -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public' ORDER BY table_name"
            )
        )
        print([row[0] for row in result])


if __name__ == "__main__":
    asyncio.run(main())