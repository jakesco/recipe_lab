from .ingredient import Ingredient
from .recipe import Recipe, IngredientAmount
from .db import DB

# TODO: Modify Recipes/Ingredients

class Repository:

    def __init__(self, db_path=":memory:"):
        self._ingredients = set()
        self._recipes = set()

        try:
            self._db = DB(db_path)
            self._load_data()
        except Exception:
            pass

    def __repr__(self):
        return f"Repository({len(self._ingredients)} - ingredients, {len(self._recipes)} - recipes)"

    def _load_data(self):
        ingredients = self._db.get_all_ingredients()
        for i in ingredients:
            self._ingredients.add(
                Ingredient(
                    i['name'],
                    i['package_amount'],
                    i['package_cost'],
                    Ingredient.Type(i['type']),
                    i['unit'],
                    i['id']
                )
            )

        recipes = self._db.get_all_recipes()
        for r, ings in recipes:
            ingredient_list = [
                IngredientAmount(
                    i['amount'],
                    self.get_ingredient_by_id(i['ingredient_id'])
                ) for i in ings
            ]
            recipe = Recipe(
                r["name"],
                r['servings'],
                r['serving_unit'],
                r['sale_price'],
                ingredient_list,
                r['id']
            )
            self._recipes.add(recipe)

    def add_ingredient(self, name, package_amount, package_cost, ingredient_type_number, unit):
        ingredient = Ingredient(name, package_amount, package_cost, Ingredient.Type(ingredient_type_number), unit)
        ingredient.id = self._db.insert_ingredient(ingredient.name,
                                                   ingredient.package_amount,
                                                   ingredient.package_cost,
                                                   ingredient.type.value,
                                                   ingredient.unit)
        self._ingredients.add(ingredient)

    def add_recipe(self, recipe):
        self._recipes.add(recipe)

    def _remove_ingredient(self, ingredient):
        self._ingredients.remove(ingredient)
        self._db.delete_ingredient(ingredient.id)

    def _remove_recipe(self, recipe):
        self._recipes.remove(recipe)
        self._db.delete_recipe(recipe.id)

    def remove(self, item):
        """Remove an Ingredient or Recipe"""
        if isinstance(item, Recipe):
            self._remove_recipe(item)
        elif isinstance(item, Ingredient):
            self._remove_ingredient(item)
        else:
            raise Exception("Item must be a Recipe or Ingredient")

    def get_ingredient_by_id(self, id):
        for i in self._ingredients:
            if i.id == id:
                return i
        return None

    def get_recipe_by_id(self, id):
        for r in self._ingredients:
            if r.id == id:
                return r
        return None

    def list_ingredients(self):
        return self._ingredients

    def list_recipes(self):
        return self._recipes

