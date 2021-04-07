from enum import Enum


class Ingredient:
    class Type(Enum):
        DRY = 1
        FLUID = 2
        OTHER = 3

    def __init__(self, name, package_amount, package_cost, ingredient_type, unit=None, ingredient_id=None):
        self.id = ingredient_id
        self.name = name
        try:
            self.package_amount = float(package_amount)
        except ValueError:
            raise Exception("Package amount must be a number.")

        try:
            self.package_cost = float(package_cost)
        except ValueError:
            raise Exception("Package cost must be a number.")

        if self.package_amount <= 0:
            raise Exception("Package amount must not be less than 0.")

        if self.package_cost <= 0:
            raise Exception("Package cost must not be less than 0.")

        self.cost_per_unit = self.package_cost / self.package_amount

        if isinstance(ingredient_type, self.Type):
            self.type = ingredient_type
            if ingredient_type == self.Type.DRY:
                self.unit = "oz"
            elif ingredient_type == self.Type.FLUID:
                self.unit = "fl. oz"
            else:
                self.unit = unit
        else:
            raise Exception("Ingredient type must be of Ingredient.Type")

    def __repr__(self):
        return "Ingredient({} - {}, {}, {} {}(s), ${:.2f}, ${:.2f} per {})".format(
            self.id,
            self.name,
            self.type,
            self.package_amount,
            self.unit,
            self.package_cost,
            self.cost_per_unit,
            self.unit,
        )

    def __hash__(self):
        return hash((self.name, self.package_amount, self.package_cost, self.type))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (self.name == other.name
                and self.package_amount == other.package_amount
                and self.package_cost == other.package_cost
                and self.type == other.type)
