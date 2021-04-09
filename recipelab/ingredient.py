from enum import Enum
from . import ureg, Q_, UndefinedUnitError


class Ingredient:
    def __init__(self, ingredient_id: int, name: str, package_amount: float, unit: str, package_cost: float):
        self.__id = ingredient_id
        self.__name = name

        try:
            amount = float(package_amount)
            if amount <= 0:
                raise Exception("Package amount must not be less than 0.")
            self.__amount = Q_(amount, unit)
        except ValueError:
            raise Exception("Package amount must be a number.")
        except UndefinedUnitError:
            # This is a hack, custom values are defined as nits.
            # It prevents conversions to other types assuming no need
            # to calculate the luminance of any food.
            ureg.define(f"{unit} = 1 nit")
            self.__amount = Q_(package_amount, unit)

        try:
            cost = float(package_cost)
            if cost <= 0:
                raise Exception("Package cost must not be less than 0.")
            self.__cost = float(package_cost)
        except ValueError:
            raise Exception("Package cost must be a number.")


    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def amount_in_package(self):
        return self.__amount

    @property
    def cost_of_package(self):
        return self.__cost

    def cost_per_unit(self, unit: str = None) -> float:
        if unit is None:
            return self.__cost / self.__amount.magnitude
        return self.__cost / self.__amount.to(unit).magnitude

    def __repr__(self):
        return "Ingredient({} - {}, {:~}(s), ${:.2f})".format(
            self.__id,
            self.__name,
            self.__amount,
            self.__cost,
        )

    def __hash__(self):
        return hash((self.__id, self.__name, self.__amount, self.__cost))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (self.__id == other.id
                and self.__name == other.name
                and self.__amount == other.amount_in_package
                and self.__cost == other.cost_of_package)