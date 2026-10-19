# scripts/seed_teams.py
import asyncio
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.team import Team


async def main() -> None:
    teams = [
        {"name": "San Lorenzo", "short_name": "CASLA", "logo_url": None},
        {"name": "Boca Juniors", "short_name": "CABJ", "logo_url": None},
        {"name": "River Plate", "short_name": "CARP", "logo_url": None},
    ]

    async with AsyncSessionLocal() as session:
        for data in teams:
            existing = await session.execute(
                select(Team).where(Team.name == data["name"])
            )
            if existing.scalar_one_or_none() is None:
                session.add(Team(**data))
                print(f"  + {data['name']}")
            else:
                print(f"  = {data['name']} (ya existía)")
        await session.commit()
        print("✅ Seed completo.")


if __name__ == "__main__":
    asyncio.run(main())