import asyncio
import os
from database import create_tables
from services.auth_service import AuthService
from database import SessionLocal

async def init_database():
    """Initialize database with tables and admin user"""
    print("Creating database tables...")
    await create_tables()
    print("Database tables created successfully")
    
    # Create admin user if configured
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    
    if admin_email and admin_password:
        auth_service = AuthService()
        async with SessionLocal() as db:
            existing_admin = await auth_service.get_user_by_email(db, admin_email)
            if not existing_admin:
                admin_user = await auth_service.create_user(
                    db, admin_email, admin_password, is_admin=True
                )
                print(f"Admin user created: {admin_email}")
            else:
                print(f"Admin user already exists: {admin_email}")

if __name__ == "__main__":
    asyncio.run(init_database())
