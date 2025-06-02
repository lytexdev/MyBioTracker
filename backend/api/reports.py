from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from datetime import datetime, date, timedelta
from typing import Optional
import json
import csv
import io

from database import get_session
from models.user import User
from models.nutrition import Meal, NutritionEntry, FoodItem
from models.caffeine import CaffeineEntry, CaffeineProduct
from api.auth import get_current_user

router = APIRouter()

@router.get("/nutrition/weekly")
async def get_weekly_nutrition_report(
    weeks_back: int = Query(4, ge=1, le=12),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Get weekly nutrition statistics"""
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(weeks=weeks_back)
    
    # Get nutrition data
    query = select(
        func.date(Meal.eaten_at).label('date'),
        func.sum(FoodItem.calories_per_100g * NutritionEntry.amount_grams / 100).label('calories'),
        func.sum(FoodItem.protein_per_100g * NutritionEntry.amount_grams / 100).label('protein'),
        func.sum(FoodItem.carbs_per_100g * NutritionEntry.amount_grams / 100).label('carbs'),
        func.sum(FoodItem.fat_per_100g * NutritionEntry.amount_grams / 100).label('fat')
    ).select_from(
        NutritionEntry.__table__.join(FoodItem).join(Meal)
    ).where(
        and_(
            NutritionEntry.user_id == current_user.id,
            func.date(Meal.eaten_at) >= start_date,
            func.date(Meal.eaten_at) <= end_date
        )
    ).group_by(func.date(Meal.eaten_at))
    
    result = await db.execute(query)
    daily_data = result.all()
    
    # Group by weeks
    weekly_data = {}
    for row in daily_data:
        week_start = row.date - timedelta(days=row.date.weekday())
        week_key = week_start.isoformat()
        
        if week_key not in weekly_data:
            weekly_data[week_key] = {
                'week_start': week_key,
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0,
                'days': 0
            }
        
        weekly_data[week_key]['calories'] += float(row.calories or 0)
        weekly_data[week_key]['protein'] += float(row.protein or 0)
        weekly_data[week_key]['carbs'] += float(row.carbs or 0)
        weekly_data[week_key]['fat'] += float(row.fat or 0)
        weekly_data[week_key]['days'] += 1
    
    # Calculate averages
    for week in weekly_data.values():
        if week['days'] > 0:
            week['avg_calories'] = round(week['calories'] / week['days'], 1)
            week['avg_protein'] = round(week['protein'] / week['days'], 1)
            week['avg_carbs'] = round(week['carbs'] / week['days'], 1)
            week['avg_fat'] = round(week['fat'] / week['days'], 1)
    
    return list(weekly_data.values())

@router.get("/caffeine/trends")
async def get_caffeine_trends(
    days_back: int = Query(30, ge=1, le=90),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Get caffeine consumption trends"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days_back)
    
    # Get caffeine data
    query = select(
        func.date(CaffeineEntry.consumed_at).label('date'),
        func.count(CaffeineEntry.id).label('entries'),
        func.sum(CaffeineProduct.caffeine_mg_per_serving * CaffeineEntry.amount_servings).label('total_caffeine'),
        func.avg(CaffeineProduct.caffeine_mg_per_serving * CaffeineEntry.amount_servings).label('avg_per_entry')
    ).select_from(
        CaffeineEntry.__table__.join(CaffeineProduct)
    ).where(
        and_(
            CaffeineEntry.user_id == current_user.id,
            CaffeineEntry.consumed_at >= start_date,
            CaffeineEntry.consumed_at <= end_date
        )
    ).group_by(func.date(CaffeineEntry.consumed_at))
    
    result = await db.execute(query)
    daily_data = result.all()
    
    # Format data
    trends = []
    for row in daily_data:
        trends.append({
            'date': row.date.isoformat(),
            'entries': row.entries,
            'total_caffeine': round(float(row.total_caffeine or 0), 1),
            'avg_per_entry': round(float(row.avg_per_entry or 0), 1)
        })
    
    return trends

@router.get("/export/nutrition")
async def export_nutrition_data(
    format: str = Query("csv", regex="^(csv|json)$"),
    days_back: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Export nutrition data"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days_back)
    
    # Get detailed nutrition data
    query = select(
        Meal.eaten_at,
        Meal.name.label('meal_name'),
        Meal.meal_type,
        FoodItem.name.label('food_name'),
        FoodItem.brand,
        NutritionEntry.amount_grams,
        (FoodItem.calories_per_100g * NutritionEntry.amount_grams / 100).label('calories'),
        (FoodItem.protein_per_100g * NutritionEntry.amount_grams / 100).label('protein'),
        (FoodItem.carbs_per_100g * NutritionEntry.amount_grams / 100).label('carbs'),
        (FoodItem.fat_per_100g * NutritionEntry.amount_grams / 100).label('fat')
    ).select_from(
        NutritionEntry.__table__.join(FoodItem).join(Meal)
    ).where(
        and_(
            NutritionEntry.user_id == current_user.id,
            Meal.eaten_at >= start_date,
            Meal.eaten_at <= end_date
        )
    ).order_by(Meal.eaten_at.desc())
    
    result = await db.execute(query)
    data = result.all()
    
    if format == "json":
        # Export as JSON
        json_data = []
        for row in data:
            json_data.append({
                'eaten_at': row.eaten_at.isoformat(),
                'meal_name': row.meal_name,
                'meal_type': row.meal_type,
                'food_name': row.food_name,
                'brand': row.brand,
                'amount_grams': float(row.amount_grams),
                'calories': round(float(row.calories or 0), 1),
                'protein': round(float(row.protein or 0), 1),
                'carbs': round(float(row.carbs or 0), 1),
                'fat': round(float(row.fat or 0), 1)
            })
        
        json_str = json.dumps(json_data, indent=2)
        return StreamingResponse(
            io.StringIO(json_str),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=nutrition_export.json"}
        )
    
    else:
        # Export as CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Date', 'Meal Name', 'Meal Type', 'Food Name', 'Brand',
            'Amount (g)', 'Calories', 'Protein (g)', 'Carbs (g)', 'Fat (g)'
        ])
        
        # Write data
        for row in data:
            writer.writerow([
                row.eaten_at.isoformat(),
                row.meal_name,
                row.meal_type,
                row.food_name,
                row.brand or '',
                round(float(row.amount_grams), 1),
                round(float(row.calories or 0), 1),
                round(float(row.protein or 0), 1),
                round(float(row.carbs or 0), 1),
                round(float(row.fat or 0), 1)
            ])
        
        output.seek(0)
        return StreamingResponse(
            io.StringIO(output.getvalue()),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=nutrition_export.csv"}
        )
