from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class CaffeineProductCreate(BaseModel):
    name: str
    category: str  # coffee, tea, energy_drink, supplement
    caffeine_mg_per_serving: float
    serving_size_ml: Optional[float] = None
    half_life_hours: float = 5.0

class CaffeineProductResponse(BaseModel):
    id: int
    name: str
    category: str
    caffeine_mg_per_serving: float
    serving_size_ml: Optional[float]
    half_life_hours: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class CaffeineEntryCreate(BaseModel):
    product_id: int
    consumed_at: datetime
    amount_servings: float = 1.0
    notes: Optional[str] = None

class CaffeineEntryResponse(BaseModel):
    id: int
    product_id: int
    consumed_at: datetime
    amount_servings: float
    notes: Optional[str]
    created_at: datetime
    product: CaffeineProductResponse
    
    class Config:
        from_attributes = True

class CaffeineLevelResponse(BaseModel):
    current_level_mg: float
    active_entries: List[Dict[str, Any]]
    calculated_at: datetime

class CaffeineCurveResponse(BaseModel):
    data_points: List[Dict[str, Any]]
    generated_at: datetime
    hours_back: int
    hours_forward: int
