from typing import List
from models import SaveRecipeDTO, RecipeDTO


class RepositoryInterface:

    def connect(self):
        pass

    def disconnect(self):
        pass

    def test_connection(self):
        pass

    def initialize(self):
        pass

    def get_recipe(self, recipe_id: int) -> RecipeDTO:
        raise NotImplementedError

    def create_recipe(self, recipe: SaveRecipeDTO) -> None:
        raise NotImplementedError

    def update_recipe(self, recipe: RecipeDTO) -> None:
        raise NotImplementedError

    def delete_recipe(self, recipe_id: int) -> None:
        raise NotImplementedError

    def check_if_recipe_exist(self, recipe_id: int) -> bool:
        raise NotImplementedError

    def get_recipes(self) -> List[RecipeDTO]:
        raise NotImplementedError

    def search_recipes(self, search: str) -> List[RecipeDTO]:
        raise NotImplementedError


