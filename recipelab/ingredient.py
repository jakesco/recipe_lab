from enum import Enum


class Ingredient:
    class Type(Enum):
        DRY = 1
        FLUID = 2
        OTHER = 3

    def __init__(self, name, package_amount, package_cost, type, unit=None):
        self.id = id
        self.name = name
        self.package_amount = float(package_amount)
        self.package_cost = package_cost
        self.cost_per_unit = self.package_cost / self.package_amount
        self.type = type

        if type == self.Type.DRY:
            self.unit = "oz"
        elif type == self.Type.FLUID:
            self.unit = "fl. oz"
        else:
            self.unit = unit

    def __repr__(self):
        return "Ingredient({}, {}, {} {}(s), ${:.2f}, ${:.2f} per {})".format(
            self.name,
            self.type,
            self.package_amount,
            self.unit,
            self.package_cost,
            self.cost_per_unit,
            self.unit,
        )
