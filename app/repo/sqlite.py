import sqlite3
import json
from .base import RepositoryInterface
from ..models import RecipeDTO, CreateRecipeDTO
from datetime import datetime
from typing import List


class SqliteRepository(RepositoryInterface):

    def __init__(self, database_url):
        self.url = database_url
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.url, check_same_thread=False)
        except sqlite3.Error as e:
            print(e)

    def disconnect(self):
        self.connection.close()

    def test_connection(self):
        self.connect()
        if self.connection:
            self.connection.close()
            return True
        return False

    def initialize(self) -> bool:
        self.connect()
        if not self.connection:
            return False
        cur = self.connection.cursor()

        try:
            cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
            tables = {row[0] for row in cur.fetchall()}
            if "recipes" not in tables:
                cur.execute("""CREATE TABLE recipes(
                                    id integer UNIQUE PRIMARY KEY, 
                                    name VARCHAR(100) NOT NULL,
                                    description text,
                                    ingredients json,
                                    timestamp integer
                                )"""  # TODO timestamp for creation or update text NOT NUll
                            )
            # if "ingredients" not in tables:
            #     cur.execute("""CREATE TABLE ingredients(
            #                        id integer Unique PRIMARY KEY,
            #                        recipe_id integer NOT NULL,
            #                        ingredient_dict text NOT NULL,
            #                        FOREIGN KEY (recipe_id) REFERENCES recipes(id)
            #                    )""") # Or every ingredient on its own quantity&desc
        finally:
            self.connection.commit()
        return True

    def get_recipe(self, recipe_id: int) -> RecipeDTO:
        cur = self.connection.cursor()
        cur.execute("SELECT id, name, description, ingredients, timestamp FROM recipes WHERE id=?", (recipe_id, ))
        row = cur.fetchone()
        cur.close()
        return RecipeDTO(id=row[0], name=row[1], description=row[2], ingredients=json.loads(row[3]),
                         timestamp=datetime.fromtimestamp(row[4]))

    def create_recipe(self, recipe: CreateRecipeDTO) -> None:
        cur = self.connection.cursor()
        # ingredients = jsonable_encoder(CreateRecipeDTO)["ingredients"]
        cur.execute("INSERT INTO recipes(name, description, ingredients, timestamp) VALUES (?, ?, ?, ?)",
                    (recipe.name, recipe.description, json.dumps(recipe.ingredients), recipe.timestamp.timestamp()))
        self.connection.commit()

    def update_recipe(self, recipe: RecipeDTO) -> None:
        cur = self.connection.cursor()
        cur.execute("UPDATE recipes SET name = ?, description = ?, ingredients = ?, timestamp = ? WHERE id = ?",
                    (recipe.name, recipe.description, json.dumps(recipe.ingredients), recipe.timestamp.timestamp(),
                     recipe.id))
        self.connection.commit()

    def delete_recipe(self, recipe_id: int) -> None:
        cur = self.connection.cursor()
        cur.execute("DELETE FROM recipes WHERE id = ?", (recipe_id, ))
        self.connection.commit()

    def check_if_recipe_exist(self, recipe_id: int) -> bool:
        cur = self.connection.cursor()
        cur.execute("SELECT id, name, description, ingredients FROM recipes WHERE id = ?", (recipe_id, ))
        row = cur.fetchone()
        cur.close()
        if row is None:
            return False
        return True

    def get_recipes(self, limit: int, offset: int) -> List[RecipeDTO]:
        cur = self.connection.cursor()
        sql = f"""SELECT id, name, description, ingredients, timestamp FROM recipes
         ORDER BY timestamp desc LIMIT {limit} OFFSET {offset}"""
        cur.execute(sql)
        rows = cur.fetchall()
        return [RecipeDTO(id=row[0], name=row[1], description=row[2], ingredients=json.loads(row[3]),
                          timestamp=datetime.fromtimestamp(row[4])) for row in rows]


