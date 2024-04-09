import sqlite3
import json
import os
from .base import RepositoryInterface
from models import RecipeDTO, SaveRecipeDTO
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
                                    category text,
                                    timestamp integer
                                )"""  # TODO timestamp for creation or update text NOT NUll
                            )
                self.connection.commit()
                self.create_data()
        finally:
            self.disconnect()
        return True

    def create_data(self) -> None:
        with open("../recipes.json") as recipe_file:
            recipes_list = json.load(recipe_file)
        for recipe in recipes_list:
            recipeDTO = SaveRecipeDTO(name=recipe["name"],
                                        description=recipe["description"],
                                        ingredients=recipe["ingredients"],
                                        category=recipe["category"],
                                        )
            self.create_recipe(recipeDTO)

    def get_recipe(self, recipe_id: int) -> RecipeDTO:
        self.connect()
        cur = self.connection.cursor()
        cur.execute("SELECT id, name, description, ingredients, category, timestamp FROM recipes WHERE id=?", (recipe_id, ))
        row = cur.fetchone()
        cur.close()
        self.disconnect()
        return RecipeDTO(id=row[0], name=row[1], description=row[2], ingredients=list(json.loads(row[3]).values()), category=row[4],
                         timestamp=datetime.fromtimestamp(row[5]))

    def create_recipe(self, recipe: SaveRecipeDTO) -> None:
        self.connect()
        cur = self.connection.cursor()
        cur.execute("INSERT INTO recipes(name, description, ingredients, category, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (recipe.name, recipe.description, json.dumps(recipe.ingredients), recipe.category, recipe.timestamp.timestamp()))
        self.connection.commit()
        self.disconnect()

    def update_recipe(self, recipe: RecipeDTO) -> None:
        self.connect()
        cur = self.connection.cursor()
        cur.execute("UPDATE recipes SET name = ?, description = ?, ingredients = ?, category = ?, timestamp = ? WHERE id = ?",
                    (recipe.name, recipe.description, json.dumps(recipe.ingredients), recipe.category, recipe.timestamp.timestamp(),
                     recipe.id))
        self.connection.commit()
        self.disconnect()

    def delete_recipe(self, recipe_id: int) -> None:
        self.connect()
        cur = self.connection.cursor()
        cur.execute("DELETE FROM recipes WHERE id = ?", (recipe_id, ))
        self.connection.commit()
        self.disconnect()

    def check_if_recipe_exist(self, recipe_id: int) -> bool:
        self.connect()
        cur = self.connection.cursor()
        cur.execute("SELECT id, name, description, ingredients, category FROM recipes WHERE id = ?", (recipe_id, ))
        row = cur.fetchone()
        cur.close()
        self.disconnect()
        if row is None:
            return False
        return True

    def get_recipes(self) -> List[RecipeDTO]:
        self.connect()
        cur = self.connection.cursor()
        sql = f"""SELECT id, name, description, ingredients, category, timestamp FROM recipes
         ORDER BY timestamp desc """ #LIMIT {limit} OFFSET {offset}
        cur.execute(sql)
        rows = cur.fetchall()
        self.disconnect()
        return [RecipeDTO(id=row[0], name=row[1], description=row[2], ingredients=list(json.loads(row[3]).values()),
                          category=row[4], timestamp=datetime.fromtimestamp(row[5])) for row in rows]

    def search_recipes(self, search: str) -> List[RecipeDTO]:
        self.connect()
        cur = self.connection.cursor()
        sql = f"""SELECT id, name, description, ingredients, category, timestamp FROM recipes 
        WHERE name LIKE ? OR ingredients LIKE ? OR category LIKE ?
        ORDER BY timestamp desc """ # LIMIT {limit} OFFSET {offset}
        search_term = f"%{search}%"
        cur.execute(sql, (search_term, search_term, search_term,))
        rows = cur.fetchall()
        self.disconnect()
        return [RecipeDTO(id=row[0], name=row[1], description=row[2], ingredients=json.loads(row[3]), category=row[4],
                          timestamp=datetime.fromtimestamp(row[5])) for row in rows]


