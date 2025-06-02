from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import asyncio
import os
from contextlib import asynccontextmanager

from database import create_tables, get_session
from api.auth import router as auth_router
from api.nutrition import router as nutrition_router
from api.caffeine import router as caffeine_router
from api.admin import router as admin_router
from api.profile import router as profile_router
from api.reports import router as reports_router
from services.food_db_service import FoodDatabaseService
from services.scheduler import start_scheduler

limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting MyBioTracker...")
    
    try:
        # Initialize database
        await create_tables()
        print("✅ Database tables created")
        
        # Initialize food database
        food_service = FoodDatabaseService()
        await food_service.initialize_food_database()
        print("✅ Food database initialized")
        
        # Start background scheduler
        start_scheduler()
        print("✅ Background scheduler started")
        
        print("🎉 MyBioTracker started successfully!")
        
    except Exception as e:
        print(f"❌ Startup error: {e}")
        raise
    
    yield
    
    # Shutdown
    print("Shutting down MyBioTracker...")

app = FastAPI(
    title="MyBioTracker",
    description="Privacy-focused nutrition and biohacking tracker",
    version="1.0.0",
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if os.getenv("ENVIRONMENT") == "development" else ["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Only add TrustedHostMiddleware in production
if os.getenv("ENVIRONMENT") != "development":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["yourdomain.com", "www.yourdomain.com"]
    )

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(nutrition_router, prefix="/api/nutrition", tags=["Nutrition"])
app.include_router(caffeine_router, prefix="/api/caffeine", tags=["Caffeine"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])
app.include_router(profile_router, prefix="/api/profile", tags=["Profile"])
app.include_router(reports_router, prefix="/api/reports", tags=["Reports"])

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/api/")
async def root():
    return {"message": "MyBioTracker API", "version": "1.0.0"}

if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
