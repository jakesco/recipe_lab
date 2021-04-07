from recipe import Recipe
from ingredient import Ingredient
from db import DB


class Repository:

    def __init__(self, db_path=":memory:"):
        self._ingredients = set()
        self._recipes = set()

        try:
            self._db = DB(db_path)
        except Exception:
            pass

    def __repr__(self):
        return f"Repository({len(self._ingredients)} - ingredients, {self._recipes} - recipes)"

    def

# Ingredient repo

# Recipe repo

# Store Ingredients/Recipes

# Add/remove recipe

# Add/remove Ingredient

# Edit recipe/ingredient

