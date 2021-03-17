from .db import DB
from .recipe import Recipe
from .ingredient import Ingredient


class RecipeLab:
    def __init__(self, db_path):
        self.db = DB(db_path)
        self.db.init_db()

    def new_ingredient(self, name, amount_per_unit, price_per_unit, type, unit=None):
        self.db.insert_ingredient(
            name, amount_per_unit, price_per_unit, type.value, unit
        )

        ing = self.db.get_ingredient_by_name(name)
        return Ingredient(
            ing["name"],
            ing["amount_per_unit"],
            ing["price_per_unit"],
            Ingredient.Type(ing["type"]),
            ing["unit"],
            ing["id"],
        )
