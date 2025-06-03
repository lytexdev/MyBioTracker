from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from models.user import User
from models.profile import UserProfile
from api.auth import get_current_user
from schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse

router = APIRouter()

@router.get("", response_model=ProfileResponse)
@router.get("/", response_model=ProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Get user profile"""
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        # Create default profile
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    
    return ProfileResponse.model_validate(profile)

@router.post("", response_model=ProfileResponse)
@router.post("/", response_model=ProfileResponse)
async def create_or_update_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Create or update user profile"""
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if profile:
        # Update existing profile
        for field, value in profile_data.model_dump(exclude_unset=True).items():
            setattr(profile, field, value)
    else:
        # Create new profile
        profile = UserProfile(
            user_id=current_user.id,
            **profile_data.model_dump()
        )
        db.add(profile)
    
    # Calculate nutritional targets
    profile = calculate_nutrition_targets(profile)
    
    await db.commit()
    await db.refresh(profile)
    
    return ProfileResponse.model_validate(profile)

@router.put("", response_model=ProfileResponse)
@router.put("/", response_model=ProfileResponse)
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Update user profile"""
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Update profile fields
    for field, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    
    # Recalculate nutritional targets
    profile = calculate_nutrition_targets(profile)
    
    await db.commit()
    await db.refresh(profile)
    
    return ProfileResponse.model_validate(profile)

def calculate_nutrition_targets(profile: UserProfile) -> UserProfile:
    """Calculate BMR, TDEE, and macro targets based on profile data"""
    if not all([profile.age, profile.weight_kg, profile.height_cm, profile.gender]):
        return profile
    
    # Calculate BMR using Mifflin-St Jeor Equation
    if profile.gender.value == "male":
        bmr = (10 * profile.weight_kg) + (6.25 * profile.height_cm) - (5 * profile.age) + 5
    else:
        bmr = (10 * profile.weight_kg) + (6.25 * profile.height_cm) - (5 * profile.age) - 161
    
    # Activity multipliers
    activity_multipliers = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725,
        "extremely_active": 1.9
    }
    
    # Calculate TDEE
    multiplier = activity_multipliers.get(profile.activity_level.value, 1.55)
    tdee = bmr * multiplier
    
    # Adjust for goals
    goal_adjustments = {
        "lose_weight": -500,
        "gain_weight": 500,
        "build_muscle": 300,
        "maintain": 0,
        "improve_health": 0
    }
    
    adjustment = goal_adjustments.get(profile.primary_goal.value, 0)
    target_calories = tdee + adjustment
    
    # Calculate macro targets (example distribution)
    protein_ratio = 0.25  # 25% protein
    fat_ratio = 0.30      # 30% fat
    carb_ratio = 0.45     # 45% carbs
    
    target_protein = (target_calories * protein_ratio) / 4  # 4 cal/g protein
    target_fat = (target_calories * fat_ratio) / 9          # 9 cal/g fat
    target_carbs = (target_calories * carb_ratio) / 4       # 4 cal/g carbs
    
    # Update profile
    profile.bmr_calories = round(bmr)
    profile.tdee_calories = round(tdee)
    profile.target_calories = round(target_calories)
    profile.target_protein_g = round(target_protein)
    profile.target_fat_g = round(target_fat)
    profile.target_carbs_g = round(target_carbs)
    
    return profile
