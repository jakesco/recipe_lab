from .db import DB
from .recipe import Recipe
from .ingredient import Ingredient


class RecipeLab:
    def __init__(self, db_path):
        self.db = DB(db_path)
        self.db.init_db()

    def __db_to_ingredient(self, db_row_ingredient):
        return Ingredient(
            db_row_ingredient["name"],
            db_row_ingredient["package_amount"],
            db_row_ingredient["package_cost"],
            Ingredient.Type(db_row_ingredient["type"]),
            db_row_ingredient["unit"],
            db_row_ingredient["id"],
        )

    def __db_to_recipe(self, db_row_recipe, db_row_recipe_ingredient):
        ings = []
        for _, ingredient_id, amount in db_row_recipe_ingredient:
            i = self.db.get_ingredient(ingredient_id)
            ings.append((amount, self.__db_to_ingredient(i)))

        return Recipe(
            db_row_recipe["name"],
            db_row_recipe["servings"],
            db_row_recipe["serving_unit"],
            db_row_recipe["sale_price"],
            ings,
            db_row_recipe["id"],
        )

    def new_ingredient(self, name, package_amount, package_cost, type, unit=None):
        ing = self.db.insert_ingredient(
            name, package_amount, package_cost, type.value, unit
        )

        return self.__db_to_ingredient(ing)

    def new_recipe(self, name, servings, serving_unit, sale_price, ingredients=[]):
        r, i = self.db.insert_recipe(
            name, servings, serving_unit, sale_price, ingredients
        )
        return self.__db_to_recipe(r, i)

    def add_ingredient_to_recipe(self, recipe, amount, ingredient):
        self.db.insert_recipe_ingredient(recipe.id, ingredient.id, amount)
        return self.__db_to_recipe(
            self.db.get_recipe(recipe.id), self.db.get_ingredients_for_recipe(recipe.id)
        )

    def list_ingredients(self):
        return list(map(self.__db_to_ingredient, self.db.get_all_ingredients()))
