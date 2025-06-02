from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, desc
from datetime import datetime, date
from typing import List, Optional
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import io
from PIL import Image

from database import get_session
from models.user import User
from models.nutrition import FoodItem, Meal, NutritionEntry
from api.auth import get_current_user
from schemas.nutrition import (
    FoodItemResponse, FoodItemCreate, MealCreate, MealResponse,
    NutritionEntryCreate, NutritionEntryResponse, DailyNutritionSummary
)

router = APIRouter()

@router.get("/foods/search", response_model=List[FoodItemResponse])
async def search_foods(
    q: str = Query(..., min_length=2),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    query = select(FoodItem).where(
        FoodItem.name.ilike(f"%{q}%")
    ).order_by(FoodItem.is_verified.desc(), FoodItem.name).limit(limit)
    
    result = await db.execute(query)
    foods = result.scalars().all()
    
    return [FoodItemResponse.model_validate(food) for food in foods]

@router.get("/foods/barcode/{barcode}", response_model=FoodItemResponse)
async def get_food_by_barcode(
    barcode: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(FoodItem).where(FoodItem.barcode == barcode)
    )
    food = result.scalar_one_or_none()
    
    if not food:
        raise HTTPException(status_code=404, detail="Food item not found")
    
    return FoodItemResponse.model_validate(food)

@router.post("/foods/scan-barcode")
async def scan_barcode(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Decode barcodes
        barcodes = decode(img)
        
        if not barcodes:
            raise HTTPException(status_code=404, detail="No barcode found in image")
        
        # Return first barcode found
        barcode_data = barcodes[0].data.decode('utf-8')
        return {"barcode": barcode_data}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

@router.post("/foods", response_model=FoodItemResponse)
async def create_food_item(
    food_data: FoodItemCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Check if barcode already exists
    if food_data.barcode:
        existing = await db.execute(
            select(FoodItem).where(FoodItem.barcode == food_data.barcode)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Barcode already exists")
    
    food_item = FoodItem(**food_data.model_dump())
    db.add(food_item)
    await db.commit()
    await db.refresh(food_item)
    
    return FoodItemResponse.model_validate(food_item)

@router.post("/meals", response_model=MealResponse)
async def create_meal(
    meal_data: MealCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    meal = Meal(
        user_id=current_user.id,
        **meal_data.model_dump()
    )
    db.add(meal)
    await db.commit()
    await db.refresh(meal)
    
    return MealResponse.model_validate(meal)

@router.get("/meals", response_model=List[MealResponse])
async def get_meals(
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    query = select(Meal).where(Meal.user_id == current_user.id)
    
    if date_from:
        query = query.where(func.date(Meal.eaten_at) >= date_from)
    if date_to:
        query = query.where(func.date(Meal.eaten_at) <= date_to)
    
    query = query.order_by(desc(Meal.eaten_at))
    
    result = await db.execute(query)
    meals = result.scalars().all()
    
    return [MealResponse.model_validate(meal) for meal in meals]

@router.post("/entries", response_model=NutritionEntryResponse)
async def create_nutrition_entry(
    entry_data: NutritionEntryCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Verify meal belongs to current user
    meal_result = await db.execute(
        select(Meal).where(
            and_(Meal.id == entry_data.meal_id, Meal.user_id == current_user.id)
        )
    )
    meal = meal_result.scalar_one_or_none()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    # Verify food item exists
    food_result = await db.execute(
        select(FoodItem).where(FoodItem.id == entry_data.food_item_id)
    )
    food_item = food_result.scalar_one_or_none()
    if not food_item:
        raise HTTPException(status_code=404, detail="Food item not found")
    
    entry = NutritionEntry(
        user_id=current_user.id,
        **entry_data.model_dump()
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry, ["food_item"])
    
    return NutritionEntryResponse.model_validate(entry)

@router.get("/summary/{target_date}", response_model=DailyNutritionSummary)
async def get_daily_nutrition_summary(
    target_date: date,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Get all entries for the date
    query = select(NutritionEntry, FoodItem).join(
        FoodItem, NutritionEntry.food_item_id == FoodItem.id
    ).join(
        Meal, NutritionEntry.meal_id == Meal.id
    ).where(
        and_(
            NutritionEntry.user_id == current_user.id,
            func.date(Meal.eaten_at) == target_date
        )
    )
    
    result = await db.execute(query)
    entries_with_food = result.all()
    
    # Calculate totals
    totals = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0,
        "fiber": 0,
        "sugar": 0,
        "sodium": 0,
    }
    
    for entry, food_item in entries_with_food:
        multiplier = entry.amount_grams / 100
        totals["calories"] += food_item.calories_per_100g * multiplier
        totals["protein"] += food_item.protein_per_100g * multiplier
        totals["carbs"] += food_item.carbs_per_100g * multiplier
        totals["fat"] += food_item.fat_per_100g * multiplier
        totals["fiber"] += food_item.fiber_per_100g * multiplier
        totals["sugar"] += food_item.sugar_per_100g * multiplier
        totals["sodium"] += food_item.sodium_per_100g * multiplier
    
    return DailyNutritionSummary(
        date=target_date,
        **totals
    )
