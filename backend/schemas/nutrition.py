from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class FoodItemCreate(BaseModel):
    barcode: Optional[str] = None
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    calories_per_100g: float
    protein_per_100g: float = 0
    carbs_per_100g: float = 0
    fat_per_100g: float = 0
    fiber_per_100g: float = 0
    sugar_per_100g: float = 0
    sodium_per_100g: float = 0

class FoodItemResponse(BaseModel):
    id: int
    barcode: Optional[str]
    name: str
    brand: Optional[str]
    category: Optional[str]
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float
    fiber_per_100g: float
    sugar_per_100g: float
    sodium_per_100g: float
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class MealCreate(BaseModel):
    name: str
    meal_type: str  # breakfast, lunch, dinner, snack
    eaten_at: datetime
    notes: Optional[str] = None

class MealResponse(BaseModel):
    id: int
    name: str
    meal_type: str
    eaten_at: datetime
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class NutritionEntryCreate(BaseModel):
    meal_id: int
    food_item_id: int
    amount_grams: float

class NutritionEntryResponse(BaseModel):
    id: int
    meal_id: int
    food_item_id: int
    amount_grams: float
    created_at: datetime
    food_item: FoodItemResponse
    
    class Config:
        from_attributes = True

class DailyNutritionSummary(BaseModel):
    date: date
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: float
    sugar: float
    sodium: float
