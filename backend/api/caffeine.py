from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, desc
from datetime import datetime, timedelta
from typing import List, Optional
import math

from database import get_session
from models.user import User
from models.caffeine import CaffeineEntry, CaffeineProduct
from api.auth import get_current_user
from schemas.caffeine import (
    CaffeineProductResponse, CaffeineProductCreate,
    CaffeineEntryCreate, CaffeineEntryResponse,
    CaffeineCurveResponse, CaffeineLevelResponse
)

router = APIRouter()

@router.get("/products", response_model=List[CaffeineProductResponse])
async def get_caffeine_products(
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    query = select(CaffeineProduct)
    
    if category:
        query = query.where(CaffeineProduct.category == category)
    
    query = query.order_by(CaffeineProduct.category, CaffeineProduct.name)
    
    result = await db.execute(query)
    products = result.scalars().all()
    
    return [CaffeineProductResponse.model_validate(product) for product in products]

@router.post("/products", response_model=CaffeineProductResponse)
async def create_caffeine_product(
    product_data: CaffeineProductCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    product = CaffeineProduct(**product_data.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    
    return CaffeineProductResponse.model_validate(product)

@router.post("/entries", response_model=CaffeineEntryResponse)
async def create_caffeine_entry(
    entry_data: CaffeineEntryCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Verify product exists
    product_result = await db.execute(
        select(CaffeineProduct).where(CaffeineProduct.id == entry_data.product_id)
    )
    product = product_result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Caffeine product not found")
    
    entry = CaffeineEntry(
        user_id=current_user.id,
        **entry_data.model_dump()
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry, ["product"])
    
    return CaffeineEntryResponse.model_validate(entry)

@router.get("/entries", response_model=List[CaffeineEntryResponse])
async def get_caffeine_entries(
    hours_back: int = Query(24, le=168),  # Max 1 week
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
    
    query = select(CaffeineEntry).where(
        and_(
            CaffeineEntry.user_id == current_user.id,
            CaffeineEntry.consumed_at >= cutoff_time
        )
    ).order_by(desc(CaffeineEntry.consumed_at))
    
    result = await db.execute(query)
    entries = result.scalars().all()
    
    return [CaffeineEntryResponse.model_validate(entry) for entry in entries]

@router.get("/current-level", response_model=CaffeineLevelResponse)
async def get_current_caffeine_level(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Calculate current caffeine level based on half-life decay"""
    now = datetime.utcnow()
    
    # Get entries from last 24 hours (caffeine is mostly gone after 24h)
    cutoff_time = now - timedelta(hours=24)
    
    query = select(CaffeineEntry, CaffeineProduct).join(
        CaffeineProduct, CaffeineEntry.product_id == CaffeineProduct.id
    ).where(
        and_(
            CaffeineEntry.user_id == current_user.id,
            CaffeineEntry.consumed_at >= cutoff_time
        )
    )
    
    result = await db.execute(query)
    entries_with_products = result.all()
    
    total_caffeine = 0
    active_entries = []
    
    for entry, product in entries_with_products:
        hours_elapsed = (now - entry.consumed_at).total_seconds() / 3600
        
        # Calculate remaining caffeine using exponential decay
        # Formula: remaining = initial * (0.5 ^ (time_elapsed / half_life))
        initial_amount = product.caffeine_mg_per_serving * entry.amount_servings
        remaining = initial_amount * (0.5 ** (hours_elapsed / product.half_life_hours))
        
        if remaining > 1:  # Only count if more than 1mg remaining
            total_caffeine += remaining
            active_entries.append({
                "product_name": product.name,
                "consumed_at": entry.consumed_at,
                "initial_mg": initial_amount,
                "remaining_mg": round(remaining, 1),
                "hours_ago": round(hours_elapsed, 1)
            })
    
    return CaffeineLevelResponse(
        current_level_mg=round(total_caffeine, 1),
        active_entries=active_entries,
        calculated_at=now
    )

@router.get("/curve", response_model=CaffeineCurveResponse)
async def get_caffeine_curve(
    hours_back: int = Query(12, le=24),
    hours_forward: int = Query(12, le=24),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Generate caffeine curve showing past and predicted future levels"""
    now = datetime.utcnow()
    start_time = now - timedelta(hours=hours_back)
    end_time = now + timedelta(hours=hours_forward)
    
    # Get relevant entries
    query = select(CaffeineEntry, CaffeineProduct).join(
        CaffeineProduct, CaffeineEntry.product_id == CaffeineProduct.id
    ).where(
        and_(
            CaffeineEntry.user_id == current_user.id,
            CaffeineEntry.consumed_at >= start_time - timedelta(hours=24)  # Include older entries that still affect curve
        )
    )
    
    result = await db.execute(query)
    entries_with_products = result.all()
    
    # Generate data points every 30 minutes
    data_points = []
    current_time = start_time
    
    while current_time <= end_time:
        total_caffeine = 0
        
        for entry, product in entries_with_products:
            if entry.consumed_at <= current_time:
                hours_elapsed = (current_time - entry.consumed_at).total_seconds() / 3600
                initial_amount = product.caffeine_mg_per_serving * entry.amount_servings
                remaining = initial_amount * (0.5 ** (hours_elapsed / product.half_life_hours))
                
                if remaining > 0.1:  # Include very small amounts for curve smoothness
                    total_caffeine += remaining
        
        data_points.append({
            "time": current_time,
            "caffeine_mg": round(total_caffeine, 1),
            "is_future": current_time > now
        })
        
        current_time += timedelta(minutes=30)
    
    return CaffeineCurveResponse(
        data_points=data_points,
        generated_at=now,
        hours_back=hours_back,
        hours_forward=hours_forward
    )

@router.delete("/entries/{entry_id}")
async def delete_caffeine_entry(
    entry_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(CaffeineEntry).where(
            and_(
                CaffeineEntry.id == entry_id,
                CaffeineEntry.user_id == current_user.id
            )
        )
    )
    entry = result.scalar_one_or_none()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Caffeine entry not found")
    
    await db.delete(entry)
    await db.commit()
    
    return {"message": "Entry deleted successfully"}
