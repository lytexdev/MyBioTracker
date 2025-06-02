import asyncio
import gzip
import json
import requests
import os
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import SessionLocal
from models.nutrition import FoodItem

class FoodDatabaseService:
    def __init__(self):
        self.openfoodfacts_url = "https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.jsonl.gz"
        self.data_dir = "data"
        self.food_db_file = os.path.join(self.data_dir, "openfoodfacts.jsonl.gz")
        
    async def initialize_food_database(self):
        """Initialize food database if empty or outdated"""
        async with SessionLocal() as db:
            result = await db.execute(select(func.count(FoodItem.id)))
            count = result.scalar()
            
            if count == 0:
                print("Food database empty, initializing...")
                await self.download_and_import_food_data()
            else:
                print(f"Food database contains {count} items")
    
    async def download_and_import_food_data(self):
        """Download OpenFoodFacts data and import to local database"""
        try:
            if not await self._download_food_data():
                await self._import_sample_food_data()
            else:
                await self._import_openfoodfacts_data()
        except Exception as e:
            print(f"Error downloading food data: {e}")
            await self._import_sample_food_data()
    
    async def _download_food_data(self) -> bool:
        """Download OpenFoodFacts database"""
        try:
            print("Downloading OpenFoodFacts database...")
            os.makedirs(self.data_dir, exist_ok=True)
            
            response = requests.get(self.openfoodfacts_url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(self.food_db_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print("Download completed")
            return True
        except Exception as e:
            print(f"Download failed: {e}")
            return False
    
    async def _import_openfoodfacts_data(self):
        """Import OpenFoodFacts data to database (sample for performance)"""
        print("Importing food data...")
        async with SessionLocal() as db:
            imported = 0
            
            try:
                with gzip.open(self.food_db_file, 'rt', encoding='utf-8') as f:
                    for line_num, line in enumerate(f):
                        if imported >= 10000:  # Limit for demo
                            break
                            
                        try:
                            product = json.loads(line.strip())
                            
                            if not self._is_valid_product(product):
                                continue
                            
                            food_item = self._create_food_item_from_product(product)
                            if food_item:
                                db.add(food_item)
                                imported += 1
                                
                                if imported % 1000 == 0:
                                    await db.commit()
                                    print(f"Imported {imported} products...")
                        
                        except json.JSONDecodeError:
                            continue
                        except Exception as e:
                            print(f"Error processing product: {e}")
                            continue
                
                await db.commit()
                print(f"Successfully imported {imported} food items")
                
            except Exception as e:
                print(f"Error importing food data: {e}")
                await self._import_sample_food_data()
    
    async def _import_sample_food_data(self):
        """Import sample food data if OpenFoodFacts fails"""
        print("Importing sample food data...")
        async with SessionLocal() as db:
            sample_foods = [
                {
                    "name": "Banana", "brand": "Generic", "category": "Fruits",
                    "calories": 89, "protein": 1.1, "carbs": 22.8, "fat": 0.3,
                    "fiber": 2.6, "sugar": 12.2, "potassium": 358, "vitamin_c": 8.7
                },
                {
                    "name": "Chicken Breast", "brand": "Generic", "category": "Meat",
                    "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6,
                    "fiber": 0, "sugar": 0, "sodium": 74
                },
                {
                    "name": "Brown Rice", "brand": "Generic", "category": "Grains",
                    "calories": 111, "protein": 2.6, "carbs": 23, "fat": 0.9,
                    "fiber": 1.8, "magnesium": 43
                },
                {
                    "name": "Broccoli", "brand": "Generic", "category": "Vegetables",
                    "calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4,
                    "fiber": 2.6, "vitamin_c": 89.2, "vitamin_k": 101.6
                },
                {
                    "name": "Whole Milk", "brand": "Generic", "category": "Dairy",
                    "calories": 61, "protein": 3.2, "carbs": 4.8, "fat": 3.3,
                    "calcium": 113, "vitamin_d": 1.3
                },
                {
                    "name": "Eggs", "brand": "Generic", "category": "Protein",
                    "calories": 155, "protein": 13, "carbs": 1.1, "fat": 11,
                    "vitamin_b12": 0.9, "selenium": 15.4
                },
                {
                    "name": "Avocado", "brand": "Generic", "category": "Fruits",
                    "calories": 160, "protein": 2, "carbs": 8.5, "fat": 14.7,
                    "fiber": 6.7, "potassium": 485, "vitamin_k": 21
                },
                {
                    "name": "Salmon", "brand": "Generic", "category": "Fish",
                    "calories": 208, "protein": 25.4, "carbs": 0, "fat": 12.4,
                    "vitamin_d": 11, "vitamin_b12": 2.8
                },
                {
                    "name": "Oats", "brand": "Generic", "category": "Grains",
                    "calories": 389, "protein": 16.9, "carbs": 66.3, "fat": 6.9,
                    "fiber": 10.6, "magnesium": 177
                },
                {
                    "name": "Spinach", "brand": "Generic", "category": "Vegetables",
                    "calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4,
                    "vitamin_k": 482.9, "folate": 194, "iron": 2.7
                }
            ]
            
            for food_data in sample_foods:
                food_item = FoodItem(
                    name=food_data["name"],
                    brand=food_data["brand"],
                    category=food_data["category"],
                    calories_per_100g=food_data["calories"],
                    protein_per_100g=food_data.get("protein", 0),
                    carbs_per_100g=food_data.get("carbs", 0),
                    fat_per_100g=food_data.get("fat", 0),
                    fiber_per_100g=food_data.get("fiber", 0),
                    sugar_per_100g=food_data.get("sugar", 0),
                    sodium_per_100g=food_data.get("sodium", 0),
                    vitamin_c_per_100g=food_data.get("vitamin_c", 0),
                    vitamin_d_per_100g=food_data.get("vitamin_d", 0),
                    vitamin_k_per_100g=food_data.get("vitamin_k", 0),
                    vitamin_b12_per_100g=food_data.get("vitamin_b12", 0),
                    folate_per_100g=food_data.get("folate", 0),
                    calcium_per_100g=food_data.get("calcium", 0),
                    iron_per_100g=food_data.get("iron", 0),
                    magnesium_per_100g=food_data.get("magnesium", 0),
                    potassium_per_100g=food_data.get("potassium", 0),
                    is_verified=True
                )
                db.add(food_item)
            
            await db.commit()
            print("Sample food data imported successfully")
    
    def _is_valid_product(self, product: dict) -> bool:
        """Check if product has required nutritional data"""
        nutriments = product.get('nutriments', {})
        
        return (
            product.get('product_name') and
            nutriments.get('energy-kcal_100g') is not None and
            nutriments.get('energy-kcal_100g') > 0
        )
    
    def _create_food_item_from_product(self, product: dict) -> FoodItem:
        """Create FoodItem from OpenFoodFacts product"""
        try:
            nutriments = product.get('nutriments', {})
            
            return FoodItem(
                barcode=product.get('code'),
                name=product.get('product_name', '').strip()[:255],
                brand=product.get('brands', '').strip()[:255] if product.get('brands') else None,
                category=product.get('categories_tags', [''])[0].replace('en:', '').strip()[:100] if product.get('categories_tags') else None,
                
                calories_per_100g=float(nutriments.get('energy-kcal_100g', 0)),
                protein_per_100g=float(nutriments.get('proteins_100g', 0)),
                carbs_per_100g=float(nutriments.get('carbohydrates_100g', 0)),
                fat_per_100g=float(nutriments.get('fat_100g', 0)),
                fiber_per_100g=float(nutriments.get('fiber_100g', 0)),
                sugar_per_100g=float(nutriments.get('sugars_100g', 0)),
                sodium_per_100g=float(nutriments.get('sodium_100g', 0)),
                
                vitamin_c_per_100g=float(nutriments.get('vitamin-c_100g', 0)),
                calcium_per_100g=float(nutriments.get('calcium_100g', 0)),
                iron_per_100g=float(nutriments.get('iron_100g', 0)),
                
                is_verified=False
            )
        except (ValueError, TypeError):
            return None
