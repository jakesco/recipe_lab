from enum import Enum


class Ingredient:
    class Type(Enum):
        DRY = 1
        FLUID = 2
        OTHER = 3

    def __init__(self, name, amount_per_unit, price_per_unit, type, unit=None, id=None):
        self.id = id
        self.name = name
        self.amount_per_unit = float(amount_per_unit)
        self.price_per_unit = price_per_unit
        self.type = type

        if type == self.Type.DRY:
            self.unit = "oz"
        elif type == self.Type.FLUID:
            self.unit = "fl. oz"
        else:
            self.unit = unit

    def __repr__(self):
        return f"Ingredient({self.id} - {self.name}, {self.type}, {self.amount_per_unit} {self.unit}(s), ${self.price_per_unit:.2f})"


class Recipe:
    def __init__(
        self, name, servings, serving_unit, sale_price, ingredients=[], id=None
    ):
        self.name = name
        self.servings = servings
        self.serving_unit = serving_unit
        self.sale_price = sale_price
        self.ingredients = ingredients
        self.id = id

    def __repr__(self):
        return f"Recipe({self.id} - {self.name}, {self.servings} {self.serving_unit}, ${self.sale_price:.2f}, {len(self.ingredients)} ingredients"
