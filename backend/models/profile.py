from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
import enum
from database import Base

class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class ActivityLevel(enum.Enum):
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTREMELY_ACTIVE = "extremely_active"

class Goal(enum.Enum):
    MAINTAIN = "maintain"
    LOSE_WEIGHT = "lose_weight"
    GAIN_WEIGHT = "gain_weight"
    BUILD_MUSCLE = "build_muscle"
    IMPROVE_HEALTH = "improve_health"

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Basic info
    age = Column(Integer, nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    body_fat_percentage = Column(Float, nullable=True)
    
    # Activity and goals
    activity_level = Column(Enum(ActivityLevel), default=ActivityLevel.MODERATELY_ACTIVE)
    primary_goal = Column(Enum(Goal), default=Goal.MAINTAIN)
    
    # Calculated values (updated when profile changes)
    bmr_calories = Column(Float, nullable=True)  # Basal Metabolic Rate
    tdee_calories = Column(Float, nullable=True)  # Total Daily Energy Expenditure
    target_calories = Column(Float, nullable=True)
    target_protein_g = Column(Float, nullable=True)
    target_carbs_g = Column(Float, nullable=True)
    target_fat_g = Column(Float, nullable=True)
    
    # Preferences
    metric_system = Column(String(20), default="metric")  # metric or imperial
    timezone = Column(String(50), default="UTC")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<UserProfile id={self.id} user_id={self.user_id}>"
