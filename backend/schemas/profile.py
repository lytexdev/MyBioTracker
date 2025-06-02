from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.profile import Gender, ActivityLevel, Goal

class ProfileCreate(BaseModel):
    age: Optional[int] = None
    gender: Optional[Gender] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    activity_level: Optional[ActivityLevel] = ActivityLevel.MODERATELY_ACTIVE
    primary_goal: Optional[Goal] = Goal.MAINTAIN
    metric_system: Optional[str] = "metric"
    timezone: Optional[str] = "UTC"

class ProfileUpdate(BaseModel):
    age: Optional[int] = None
    gender: Optional[Gender] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    activity_level: Optional[ActivityLevel] = None
    primary_goal: Optional[Goal] = None
    metric_system: Optional[str] = None
    timezone: Optional[str] = None

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    age: Optional[int]
    gender: Optional[Gender]
    height_cm: Optional[float]
    weight_kg: Optional[float]
    body_fat_percentage: Optional[float]
    activity_level: ActivityLevel
    primary_goal: Goal
    bmr_calories: Optional[float]
    tdee_calories: Optional[float]
    target_calories: Optional[float]
    target_protein_g: Optional[float]
    target_carbs_g: Optional[float]
    target_fat_g: Optional[float]
    metric_system: str
    timezone: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
