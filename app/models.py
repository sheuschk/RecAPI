from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime


class RecipeDTO(BaseModel):
    id: int
    name: str
    description: str
    ingredients: List[Dict]
    category: str
    timestamp: datetime | None = datetime.now()


class CreateRecipeDTO(BaseModel):
    name: str
    description: str
    ingredients: List[Dict]
    category: str
    timestamp: datetime | None = datetime.now()


class SaveRecipeDTO(BaseModel):
    id: int | None
    name: str
    description: str
    ingredients: Dict
    category: str
    timestamp: datetime | None = datetime.now()

    def update_recipe(self):
        self.timestamp = datetime.now()


class RecipeListDTO(BaseModel):
    recipes: List[RecipeDTO]
