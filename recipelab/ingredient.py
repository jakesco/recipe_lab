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
        return "Ingredient({} - {}, {}, {} {}(s), ${:.2f})".format(
            self.id,
            self.name,
            self.type,
            self.amount_per_unit,
            self.unit,
            self.price_per_unit,
        )

    def cost(self, amount):
        return round((self.price_per_unit * amount) / self.amount_per_unit, 2)
