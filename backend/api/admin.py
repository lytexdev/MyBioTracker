from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_session
from models.user import User
from api.auth import get_admin_user
from schemas.auth import UserResponse

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_session)
):
    """Get all users (admin only)"""
    from services.auth_service import AuthService
    auth_service = AuthService()
    users = await auth_service.get_all_users(db)
    return [UserResponse.model_validate(user) for user in users]

@router.post("/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_session)
):
    """Toggle user active status (admin only)"""
    from services.auth_service import AuthService
    auth_service = AuthService()
    
    user = await auth_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == admin_user.id:
        raise HTTPException(status_code=400, detail="Cannot modify your own account")
    
    await auth_service.toggle_user_active(db, user)
    
    return {
        "message": f"User {'activated' if user.is_active else 'deactivated'} successfully"
    }

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_session)
):
    """Delete user (admin only)"""
    from services.auth_service import AuthService
    auth_service = AuthService()
    
    user = await auth_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == admin_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    await auth_service.delete_user(db, user)
    
    return {"message": "User deleted successfully"}

@router.get("/stats")
async def get_admin_stats(
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_session)
):
    """Get admin dashboard statistics"""
    from sqlalchemy import func, select
    from models.nutrition import FoodItem, Meal
    from models.caffeine import CaffeineEntry
    
    # Count users
    user_count_result = await db.execute(select(func.count(User.id)))
    user_count = user_count_result.scalar()
    
    # Count foods
    food_count_result = await db.execute(select(func.count(FoodItem.id)))
    food_count = food_count_result.scalar()
    
    # Count meals
    meal_count_result = await db.execute(select(func.count(Meal.id)))
    meal_count = meal_count_result.scalar()
    
    # Count caffeine entries
    caffeine_count_result = await db.execute(select(func.count(CaffeineEntry.id)))
    caffeine_count = caffeine_count_result.scalar()
    
    return {
        "users": user_count,
        "food_items": food_count,
        "meals_logged": meal_count,
        "caffeine_entries": caffeine_count
    }
