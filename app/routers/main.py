from fastapi import APIRouter, Request, HTTPException
from ..models import RecipeListDTO
router = APIRouter()


@router.get("/", response_model=RecipeListDTO)
async def root(request: Request, limit: int = 10, offset: int = 0) -> RecipeListDTO:
    """Main Paige with recipes
    TODO's: Filter, Sort, Search
    """
    try:
        recipes = request.app.db.get_recipes(limit, offset)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Selecting Recipes was not feasible")
    recipe_list = RecipeListDTO(recipes=recipes, limit=limit, offset=offset)
    return recipe_list

