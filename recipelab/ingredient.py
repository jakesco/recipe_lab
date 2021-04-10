from recipelab import log
from recipelab import unit_registry, Q_, UndefinedUnitError, DimensionalityError


class Ingredient:
    def __init__(self, ingredient_id: int, name: str, package_amount: float, unit: str, package_cost: float):
        self.__id = ingredient_id
        self.__name = name

        try:
            amount = float(package_amount)
            if amount <= 0:
                log.exception(f"Package amount ({amount}) must be positive.")
                raise PackageAmountNotPositive()
            self.__amount = Q_(amount, unit)
        except ValueError:
            log.exception(f"Package amount ({package_amount}) must be a number.")
            raise PackageAmountNotNumber()
        except UndefinedUnitError:
            # This is a hack, custom values are defined as nits.
            # It prevents conversions to other types assuming no need
            # to calculate the luminance of any food.
            unit_registry.define(f"{unit} = 1 nit")
            self.__amount = Q_(package_amount, unit)
            log.info(f"New unit {unit} added to unit registry.")

        try:
            cost = float(package_cost)
            if cost <= 0:
                log.error(f"Package amount ({cost}) must be positive.")
                raise PackageCostNotPositive()
            self.__cost = float(package_cost)
        except ValueError:
            log.error(f"Package amount ({package_cost}) must be a number.")
            raise PackageCostNotNumber()

        log.debug(f"New ingredient created: {self}.")

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
        try:
            return self.__cost / self.__amount.to(unit).magnitude
        except DimensionalityError:
            log.error(f"Failed to convert ({self.__amount.units} -> {unit}).")
            raise IncompatibleUnitConversion(f"{self.__amount.units} -> {unit}")


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


class PackageAmountNotPositive(Exception):
    pass


class PackageAmountNotNumber(Exception):
    pass


class PackageCostNotPositive(Exception):
    pass


class PackageCostNotNumber(Exception):
    pass


class IncompatibleUnitConversion(Exception):
    pass
