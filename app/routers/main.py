from fastapi import APIRouter, Request, HTTPException, Depends
from models import SaveRecipeDTO, RecipeDTO, RecipeListDTO, CreateRecipeDTO

# TODO's: Sort (maybe on client side + discard offset and limit)

# router = APIRouter()
router = APIRouter(
    prefix="",
    tags=["recipe"],
    responses={404: {"Msg": "Not found"}}
)


def recipe_dto_id_exists(recipe: RecipeDTO, request: Request):
    recipe_id = recipe.id
    recipe_id_exists(recipe_id, request)
    return recipe


def recipe_id_exists(recipe_id, request: Request):
    if request.app.db.check_if_recipe_exist(recipe_id) is False:
        raise HTTPException(status_code=404, detail="Recipe does not exits")
    return recipe_id


@router.get("/", response_model=RecipeListDTO)
async def get_recipe_list(request: Request, search: str = None) -> RecipeListDTO:
    try:
        if search is not None:
            recipes = request.app.db.search_recipes(search)
        else:
            recipes = request.app.db.get_recipes()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Selecting Recipes was not feasible")
    recipe_list = RecipeListDTO(recipes=recipes)
    return recipe_list


@router.get("/{recipe_id}", response_model=RecipeDTO)
async def get_recipe(request: Request, recipe_id: int = Depends(recipe_id_exists)) -> RecipeDTO:
    try:
        recipe = request.app.db.get_recipe(recipe_id)
        return recipe
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="SELECT Command was not feasible")


@router.put("/")
async def update_recipe(request: Request, recipe: RecipeDTO = Depends(recipe_dto_id_exists)):
    ingredients = recipe.ingredients
    ingredient_dict = {}
    for key in range(len(ingredients)):
        ingredient_dict[key] = ingredients[key]
    new_recipe = SaveRecipeDTO(id=recipe.id, name=recipe.name, description=recipe.description, ingredients=ingredient_dict,
                               category=str(recipe.category)) #, timestamp=recipe.timestamp)
    try:
        # new_recipe.update_recipe()
        request.app.db.update_recipe(new_recipe)
        return {"Msg": "Update successful"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="DB UPDATE was not feasible")


@router.post("/")
async def create_recipe(request: Request, recipe: CreateRecipeDTO):
    ingredients = recipe.ingredients
    ingredient_dict = {}
    for key in range(len(ingredients)):
        ingredient_dict[key] = ingredients[key]
    new_recipe = SaveRecipeDTO(name=recipe.name, description=recipe.description, ingredients=ingredient_dict,
                               category=recipe.category)
    try:
        request.app.db.create_recipe(new_recipe)
        return {"Msg": "Creation successful"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="DB CREATE object was not feasible")


@router.post("/{recipe_id}")
async def delete_recipe(request: Request, recipe_id: int = Depends(recipe_id_exists)):
    try:
        request.app.db.delete_recipe(recipe_id)
        return {"Msg": "Deletion successful"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="DB DELETE was not feasible")
