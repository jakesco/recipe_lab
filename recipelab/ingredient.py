from enum import Enum


class Ingredient:
    class Type(Enum):
        DRY = 1
        FLUID = 2
        OTHER = 3

    def __init__(
        self, name, amount_per_unit, price_per_unit, ingredient_type, unit=None, id=None
    ):
        self.id = id
        self.name = name
        self.amount_per_unit = float(amount_per_unit)
        self.price_per_unit = price_per_unit
        self.ingredient_type = ingredient_type

        if ingredient_type == self.Type.DRY:
            self.unit = "oz"
        elif ingredient_type == self.Type.FLUID:
            self.unit = "fl. oz"
        else:
            self.unit = unit

    def __repr__(self):
        return f"Ingredient({self.id} - {self.name}, {self.ingredient_type}, {self.amount_per_unit} {self.unit}(s), ${self.price_per_unit:.2f})"