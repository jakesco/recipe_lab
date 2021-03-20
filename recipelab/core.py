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
        )

    def __db_to_recipe(self, db_row_recipe, db_row_recipe_ingredient):
        recipe = Recipe(
            db_row_recipe["name"],
            db_row_recipe["servings"],
            db_row_recipe["serving_unit"],
            db_row_recipe["sale_price"],
            [],
        )
        for row in db_row_recipe_ingredient:
            ingredient = self.__db_to_ingredient(row)
            recipe.add_ingredient(row["amount"], ingredient)

        return recipe

    def new_ingredient(self, name, package_amount, package_cost, type, unit=None):
        ing = self.db.insert_ingredient(
            name, package_amount, package_cost, type.value, unit
        )

        return self.__db_to_ingredient(ing)

    def get_recipe(self, name):
        r, i = self.db.get_recipe(name)
        return self.__db_to_recipe(r, i)

    def save_recipe(self, recipe):
        pass

    def list_recipes(self):
        return list(
            map(lambda r: self.__db_to_recipe(r[0], r[1]), self.db.get_all_recipes())
        )

    def list_ingredients(self):
        return list(map(self.__db_to_ingredient, self.db.get_all_ingredients()))

    def fuzzy_name_search(self, search, obj_list):
        return list(filter(lambda item: search in item.name, obj_list))
