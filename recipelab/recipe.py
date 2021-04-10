from recipelab import log
from recipelab import unit_registry, Q_, UndefinedUnitError
from recipelab.ingredient import Ingredient, IncompatibleUnitConversion
from collections import namedtuple

RecipeIngredient = namedtuple('RecipeIngredient', ["amount", "ingredient"])


class Recipe:
    def __init__(self,
                 recipe_id: int,
                 name: str,
                 servings: float,
                 serving_unit: str,
                 sale_price: str,
                 ingredients_list: list[RecipeIngredient] = None):
        self.__id = recipe_id
        self.name = name

        try:
            serv = float(servings)
            if serv <= 0:
                log.error("Recipe servings must be positive.")
                raise ServingsNotPositive()
            self.servings = Q_(serv, serving_unit)
        except ValueError:
            log.error("Recipe servings not a number.")
            raise ServingsAmountNotNumber()
        except UndefinedUnitError:
            # This is a hack, custom values are defined as nits.
            # It prevents conversions to other types assuming no need
            # to calculate the luminance of any food.
            unit_registry.define(f"{serving_unit} = 1 nit")
            self.servings = Q_(servings, serving_unit)
            log.info(f"New unit {serving_unit} added to unit registry.")

        try:
            price = float(sale_price)
            if price <= 0:
                log.error("Sale price must be positive.")
                raise SalePriceNotPositive()
            self.sale_price = price
        except ValueError:
            log.error("Sale price must be a number.")
            raise SalePriceNotNumber()

        # the ingredients are IngredientAmount named tuples
        if ingredients_list is None:
            self.__ingredients = []
        else:
            if False in [isinstance(i, RecipeIngredient) for i in ingredients_list]:
                raise IngredientListComposedOfIncorrectType()
            self.__ingredients = ingredients_list

    @property
    def id(self):
        return self.__id

    @property
    def ingredients(self):
        return self.__ingredients

    def __repr__(self):
        return "Recipe({} - {}, {:~}, ${:.2f}, {} ingredients)".format(
            self.__id,
            self.name,
            self.servings,
            self.sale_price,
            len(self.__ingredients)
        )

    def add_ingredient(self, amount: float, unit: str, ingredient: Ingredient):
        try:
            ingredient.cost_per_unit(unit)
            ingredient_amount = RecipeIngredient(Q_(amount, unit), ingredient)
            if ingredient_amount not in self.__ingredients:
                self.__ingredients.append(ingredient_amount)
                log.info(f"{ingredient_amount} added to {self.name}.")
        except IncompatibleUnitConversion as e:
            log.error(f"{unit} is not compatible with {ingredient.amount_in_package.units}.")
            raise e
        except UndefinedUnitError as e:
            log.error(f"{unit} is not a valid unit.")
            raise e

    def remove_ingredient(self, amount: float, unit: str, ingredient: Ingredient):
        # TODO: revisit this (may want to just pass index as argument)
        ingredient_amount = RecipeIngredient(Q_(amount, unit), ingredient)
        self.__ingredients = [i for i in self.__ingredients if i != ingredient_amount]
        log.info(f"{ingredient_amount} removed from {self.name}")

    def cost(self) -> float:
        sum([i.amount.magnitude * i.ingredient.cost_per_unit(i.amount.units) for i in self.__ingredients])

    def cost_per_serving(self) -> float:
        return self.cost() / self.servings.magnitude

    def profit(self) -> float:
        return self.sale_price - self.cost()


class ServingsNotPositive(Exception):
    pass


class ServingsAmountNotNumber(Exception):
    pass


class SalePriceNotPositive(Exception):
    pass


class SalePriceNotNumber(Exception):
    pass


class IngredientListComposedOfIncorrectType(Exception):
    pass