from . import log
from .ingredient import Ingredient
from .recipe import Recipe
from .db import DB


class Repository:

    def __init__(self, db_path=":memory:"):
        self._ingredients = dict()
        self._recipes = dict()

        try:
            self._db = DB(db_path)
            self.refresh()
        except Exception as e:
            log.error(f"Error loading database ({e}).")

    def __repr__(self):
        return f"Repository({len(self._ingredients)} - ingredients, {len(self._recipes)} - recipes)"

    @staticmethod
    def __db_row_to_ingredient(row: dict):
        return Ingredient(row["id"], row["name"], row["amount"], row["unit"], row["cost"])

    @staticmethod
    def __db_row_to_recipe(row: dict):
        return Recipe(row["id"], row["name"], row["servings"], row["serving_unit"], row["sale_price"])

    def refresh(self):
        self._ingredients.clear()
        self._recipes.clear()

        ingredients = self._db.get_all_ingredients()
        for i in ingredients:
            ingredient = self.__db_row_to_ingredient(i)
            self._ingredients[ingredient.id] = ingredient

        recipes = self._db.get_all_recipes()
        for r in recipes:
            recipe = self.__db_row_to_recipe(r)
            for i in r["ingredients"]:
                recipe.add_ingredient(i["amount"], i["unit"], self._ingredients[i["id"]])
            self._recipes[recipe.id] = recipe

    def new_ingredient(self, name: str, amount: float, unit: str, cost: float) -> None:
        ingredient_id = self._db.insert_ingredient(name, amount, unit, cost)
        # TODO if this second statement fails, the ingredient may still be added to db
        self._ingredients[ingredient_id] = Ingredient(ingredient_id, name, amount, unit, cost)

    def new_recipe(self, name: str, servings: float, sale_price: float, serving_unit: str = None, ingredients_list: list[tuple[int, float, str]] = None):
        recipe_id = self._db.insert_recipe(name, servings, sale_price, serving_unit, ingredients_list)
        r = self._db.get_recipes((recipe_id,))[0]
        recipe = self.__db_row_to_recipe(r)
        for i in r["ingredients"]:
            recipe.add_ingredient(i["amount"], i["unit"], self._ingredients[i["id"]])
        self._recipes[recipe_id] = recipe

    def get_ingredient(self, ingredient_id) -> Ingredient:
        return self._ingredients[ingredient_id]

    def get_recipe(self, recipe_id) -> Recipe:
        return self._recipes[recipe_id]

    def list_ingredients(self) -> list[Ingredient]:
        return list(self._ingredients.values())

    def list_recipes(self) -> list[Recipe]:
        return list(self._recipes.values())

    # TODO: Edit ingredients/recipes

    def delete_ingredient(self, ingredient_id) -> None:
        self._db.delete_ingredients((ingredient_id,))
        del self._ingredients[ingredient_id]

    def delete_recipe(self, recipe_id) -> None:
        self._db.delete_recipes((recipe_id,))
        del self._recipes[recipe_id]
