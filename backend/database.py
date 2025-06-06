from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os

# Use SQLite for local development, PostgreSQL for production
if os.getenv("ENVIRONMENT") == "production":
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://mybiotracker:mybiotracker@postgres:5432/mybiotracker")
else:
    # Local development with SQLite
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./mybiotracker.db")

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_session():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Alias for compatibility with existing code
get_db = get_session

async def create_tables():
    from models.user import User
    from models.nutrition import FoodItem, NutritionEntry, Meal
    from models.caffeine import CaffeineEntry, CaffeineProduct
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
