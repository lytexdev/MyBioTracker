from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class FoodItem(Base):
    __tablename__ = "food_items"
    
    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String(20), unique=True, index=True, nullable=True)
    name = Column(String(255), nullable=False, index=True)
    brand = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True)
    
    # Nutritional values per 100g
    calories_per_100g = Column(Float, nullable=False)
    protein_per_100g = Column(Float, default=0)
    carbs_per_100g = Column(Float, default=0)
    fat_per_100g = Column(Float, default=0)
    fiber_per_100g = Column(Float, default=0)
    sugar_per_100g = Column(Float, default=0)
    sodium_per_100g = Column(Float, default=0)
    
    # Micronutrients per 100g
    vitamin_a_per_100g = Column(Float, default=0)
    vitamin_c_per_100g = Column(Float, default=0)
    vitamin_d_per_100g = Column(Float, default=0)
    vitamin_e_per_100g = Column(Float, default=0)
    vitamin_k_per_100g = Column(Float, default=0)
    vitamin_b1_per_100g = Column(Float, default=0)
    vitamin_b2_per_100g = Column(Float, default=0)
    vitamin_b3_per_100g = Column(Float, default=0)
    vitamin_b6_per_100g = Column(Float, default=0)
    vitamin_b12_per_100g = Column(Float, default=0)
    folate_per_100g = Column(Float, default=0)
    calcium_per_100g = Column(Float, default=0)
    iron_per_100g = Column(Float, default=0)
    magnesium_per_100g = Column(Float, default=0)
    zinc_per_100g = Column(Float, default=0)
    potassium_per_100g = Column(Float, default=0)
    
    # Meta
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Meal(Base):
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    meal_type = Column(String(50), nullable=False)  # breakfast, lunch, dinner, snack
    eaten_at = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationship
    entries = relationship("NutritionEntry", back_populates="meal", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Meal(id={self.id}, user_id={self.user_id}, name={self.name}, meal_type={self.meal_type}, eaten_at={self.eaten_at})>"

class NutritionEntry(Base):
    __tablename__ = "nutrition_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    food_item_id = Column(Integer, ForeignKey("food_items.id"), nullable=False)
    amount_grams = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    food_item = relationship("FoodItem")
    meal = relationship("Meal", back_populates="entries")

    def __repr__(self):
        return f"<NutritionEntry(id={self.id}, user_id={self.user_id}, meal_id={self.meal_id}, food_item_id={self.food_item_id}, amount_grams={self.amount_grams})>"
