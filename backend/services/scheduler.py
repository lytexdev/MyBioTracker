from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import asyncio
import os
from services.food_db_service import FoodDatabaseService

scheduler = AsyncIOScheduler()

async def update_food_database():
    """Update food database from OpenFoodFacts"""
    try:
        print("Starting scheduled food database update...")
        food_service = FoodDatabaseService()
        await food_service.download_and_import_food_data()
        print("Food database update completed successfully")
    except Exception as e:
        print(f"Error updating food database: {e}")

async def cleanup_old_sessions():
    """Clean up expired sessions and tokens"""
    try:
        print("Starting session cleanup...")
        # TODO: Implement session cleanup logic
        # This would involve removing expired tokens from a blacklist
        # or cleaning up expired session data from Redis
        print("Session cleanup completed")
    except Exception as e:
        print(f"Error during session cleanup: {e}")

async def generate_daily_health_facts():
    """Generate daily health facts for users"""
    try:
        print("Generating daily health facts...")
        # Implement health facts generation
        # This could involve creating daily tips, reminders, or insights
        print("Daily health facts generated")
    except Exception as e:
        print(f"Error generating health facts: {e}")

def start_scheduler():
    """Start the background scheduler"""
    try:
        # Update food database weekly (every Sunday at 2 AM)
        if os.getenv("AUTO_UPDATE_FOOD_DB", "true").lower() == "true":
            scheduler.add_job(
                update_food_database,
                CronTrigger(day_of_week=6, hour=2, minute=0),
                id="update_food_db",
                replace_existing=True
            )

        # Clean up sessions daily at 3 AM
        scheduler.add_job(
            cleanup_old_sessions,
            CronTrigger(hour=3, minute=0),
            id="cleanup_sessions",
            replace_existing=True
        )

        # Generate health facts daily at 6 AM
        scheduler.add_job(
            generate_daily_health_facts,
            CronTrigger(hour=6, minute=0),
            id="daily_health_facts",
            replace_existing=True
        )

        scheduler.start()
        print("Background scheduler started successfully")
        
    except Exception as e:
        print(f"Error starting scheduler: {e}")

def stop_scheduler():
    """Stop the background scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        print("Background scheduler stopped")
