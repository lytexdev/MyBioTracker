import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from database import Base
from models.user import User
from models.nutrition import FoodItem, NutritionEntry, Meal
from models.caffeine import CaffeineEntry, CaffeineProduct

async def migrate_database():
    print("🔄 Starting database migration...")
    
    # Set environment
    os.environ["ENVIRONMENT"] = "development"
    
    # Create engine
    DATABASE_URL = "sqlite+aiosqlite:///./mybiotracker.db"
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    try:
        # Drop all tables first
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            print("🗑️  Dropped all existing tables")
        
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Created all tables successfully")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(migrate_database()) 