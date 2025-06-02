from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class CaffeineProduct(Base):
    __tablename__ = "caffeine_products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)  # coffee, tea, energy_drink, supplement
    caffeine_mg_per_serving = Column(Float, nullable=False)
    serving_size_ml = Column(Float, nullable=True)
    
    # Additional properties
    half_life_hours = Column(Float, default=5.0)  # Caffeine half-life varies by person
    
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<CaffeineProduct id={self.id} name={self.name} category={self.category} caffeine_mg_per_serving={self.caffeine_mg_per_serving} serving_size_ml={self.serving_size_ml}>"

class CaffeineEntry(Base):
    __tablename__ = "caffeine_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("caffeine_products.id"), nullable=False)
    
    consumed_at = Column(DateTime, nullable=False)
    amount_servings = Column(Float, default=1.0)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    product = relationship("CaffeineProduct")

    def __repr__(self):
        return f"<CaffeineEntry id={self.id} user_id={self.user_id} product_id={self.product_id} consumed_at={self.consumed_at} amount_servings={self.amount_servings} notes={self.notes}>"
