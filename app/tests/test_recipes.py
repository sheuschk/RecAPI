import os
from fastapi.testclient import TestClient
from datetime import datetime
from ..main import app
from ..config import DATETIME_FORMAT
from ..models import RecipeListDTO
# os.environ.setdefault("TEST", "True")

client = TestClient(app)

create_recipe_dto = {"name": "Name", "description": "Desc", "ingredients": {"Ing1": "1", "Ing2": 2}, "category": "Soup"}
update_recipe_dto = {"id": 1, "name": "Name1", "description": "Desc1", "ingredients": {"Ing1": "1"}, "category": "Meat"}


def test_main():
    response = client.get("/")
    assert response.status_code == 200


def test_create_recipe():
    # create_recipe_dto_json = jsonable_encoder(create_recipe_dto)
    response = client.post("/", json=create_recipe_dto)
    assert response.status_code == 200
    assert response.json() == {"Msg": "Creation successful"}


def test_get_recipe():
    response = client.get("/1")
    response_json = response.json()
    assert datetime_tester(response_json.pop("timestamp"))
    assert response.status_code == 200
    assert response_json == {"id": 1, "name": "Name", "description": "Desc", "ingredients": {"Ing1": "1", "Ing2": 2}, "category": "Soup"}


def test_update_recipe():
    response = client.put("/", json=update_recipe_dto)
    assert response.status_code == 200
    assert response.json() == {"Msg": "Update successful"}
    get_resp = client.get("/1")
    get_resp_json = get_resp.json()
    assert get_resp.status_code == 200
    assert datetime_tester(get_resp_json.pop("timestamp"))
    assert get_resp_json == update_recipe_dto


def test_delete_recipe():
    response = client.post("/1")
    print(response.json(), response.status_code)
    assert response.status_code == 200
    assert response.json() == {"Msg": "Deletion successful"}


def test_update_recipe_does_not_exist():
    client.post("/1")
    response_update = client.put("/", json=update_recipe_dto)
    response_delete = client.post("/1")
    response_create = client.get("/1")

    assert 404 == response_update.status_code == response_delete.status_code == response_create.status_code
    assert {"detail": "Recipe does not exits"} == response_update.json() == response_delete.json() \
           == response_create.json()


def test_recipe_page():
    # 1. Create recipes
    for i in range(1, 4):
        create_recipe_dto["name"] = str(i)
        client.post("/", json=create_recipe_dto)

    # 2. Test list
    response = client.get("/")
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body["recipes"]) == 3

    # Check single recipe
    recipe_1 = response_body["recipes"][0]
    assert datetime_tester(recipe_1.pop("timestamp"))
    assert recipe_1 == {"id": 1, "name": "1", "description": "Desc", "ingredients": {"Ing1": "1", "Ing2": 2},
                        "category": "Soup"}

    # Check offset
    response = client.get("/?offset=1&limit=1")
    assert len(response.json()["recipes"]) == 1
    assert response.json()["recipes"][0]["name"] == "2"


def test_search():
    create_recipe_dto["category"] = "Noodle"
    client.post("/", json=create_recipe_dto)

    response = client.get("/?search=Noo")
    assert response.status_code == 200
    assert len(response.json()["recipes"]) == 1


def test_delete_db():
    client.app.db.disconnect()
    os.remove("test.db")


# Test utils
def datetime_tester(timestamp: str):
    try:
        datetime.strptime(timestamp, DATETIME_FORMAT)
        return True
    except ValueError:
        # raise AssertionError("Datetime not in correct format")
        return False
