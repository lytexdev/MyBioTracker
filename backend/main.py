from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Include all API routers first
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

# Mount static assets (must be before catch-all route)
if os.path.exists("static"):
    # Mount assets directory for CSS, JS, fonts, etc.
    app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")
    
    # Serve specific static files
    @app.get("/manifest.json")
    async def serve_manifest():
        manifest_path = os.path.join("static", "manifest.json")
        if os.path.exists(manifest_path):
            return FileResponse(manifest_path)
        raise HTTPException(status_code=404, detail="Manifest not found")
    
    @app.get("/favicon.ico")
    async def serve_favicon():
        favicon_path = os.path.join("static", "favicon.ico")
        if os.path.exists(favicon_path):
            return FileResponse(favicon_path)
        raise HTTPException(status_code=404, detail="Favicon not found")
    
    @app.get("/logo.svg")
    async def serve_logo():
        logo_path = os.path.join("static", "logo.svg")
        if os.path.exists(logo_path):
            return FileResponse(logo_path)
        raise HTTPException(status_code=404, detail="Logo not found")

# Serve Vue.js frontend for root and all other routes (SPA)
@app.get("/")
async def serve_frontend():
    """Serve the Vue.js frontend"""
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "MyBioTracker API", "frontend": "Not built yet"}

# Catch-all route for Vue Router (must be last)
@app.get("/{path:path}")
async def catch_all(path: str):
    """Serve the Vue.js frontend for all non-API routes (SPA)"""
    # Ignore API routes
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="Page not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
