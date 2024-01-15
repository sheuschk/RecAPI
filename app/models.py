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

    def update_recipe(self):
        self.timestamp = datetime.now()


class CreateRecipeDTO(BaseModel):
    name: str
    description: str
    ingredients: List[Dict]
    category: str
    timestamp: datetime | None = datetime.now()


class SaveRecipeDTO(BaseModel):
    name: str
    description: str
    ingredients: Dict
    category: str
    timestamp: datetime | None = datetime.now()


class RecipeListDTO(BaseModel):
    offset: int | None
    limit: int | None
    recipes: List[RecipeDTO]
