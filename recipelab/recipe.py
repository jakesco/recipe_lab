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
        self.__servings = 0
        self.set_servings(servings)
        self.serving_unit = serving_unit
        self.__sale_price = 0
        self.set_sale_price(sale_price)

        # the ingredients are IngredientAmount named tuples
        if ingredients_list is None:
            self.__ingredients = []
        else:
            for i in ingredients_list:
                if not isinstance(i, RecipeIngredient):
                    raise IngredientListComposedOfIncorrectType()
            self.__ingredients = ingredients_list

        self.__cost = self.cost()

        log.debug(f"New recipe created: {self}.")

    @property
    def id(self):
        return self.__id

    @property
    def ingredients(self):
        return self.__ingredients

    @property
    def servings(self):
        return self.__servings

    @property
    def sale_price(self):
        return self.__sale_price

    def set_servings(self, servings):
        try:
            serv = float(servings)
            if serv <= 0:
                log.error("Recipe servings must be positive.")
                raise ServingsNotPositive()
            self.__servings = serv
        except ValueError:
            log.error("Recipe servings not a number.")
            raise ServingsAmountNotNumber()

    def set_sale_price(self, sale_price):
        try:
            price = float(sale_price)
            if price <= 0:
                log.error("Sale price must be positive.")
                raise SalePriceNotPositive()
            self.__sale_price = price
        except ValueError:
            log.error("Sale price must be a number.")
            raise SalePriceNotNumber()

    def __repr__(self):
        return "Recipe({} - {}, {} {}, ${:.2f}, {} ingredients)".format(
            self.__id,
            self.name,
            self.__servings,
            self.serving_unit,
            self.__sale_price,
            len(self.__ingredients)
        )

    def add_ingredient(self, amount: float, unit: str, ingredient: Ingredient):
        try:
            ingredient.cost_per_unit(unit)
            ingredient_amount = RecipeIngredient(Q_(amount, unit), ingredient)
            if ingredient_amount not in self.__ingredients:
                self.__ingredients.append(ingredient_amount)
                self.__cost = self.cost()
                log.info(f"{ingredient_amount.amount:~} {ingredient_amount.ingredient.name} added to {self.name}.")
        except IncompatibleUnitConversion as e:
            log.error(f"{unit} is not compatible with {ingredient.amount.units}.")
            raise e
        except UndefinedUnitError as e:
            log.error(f"{unit} is not a valid unit.")
            raise e

    def remove_ingredient(self, amount: float, unit: str, ingredient: Ingredient):
        # TODO: revisit this (may want to just pass id as argument)
        ingredient_amount = RecipeIngredient(Q_(amount, unit), ingredient)
        self.__ingredients = [i for i in self.__ingredients if i != ingredient_amount]
        self.__cost = self.cost()
        log.info(f"{ingredient_amount} removed from {self.name}")

    def cost(self) -> float:
        return sum([i.amount.magnitude * i.ingredient.cost_per_unit(i.amount.units) for i in self.__ingredients])

    def cost_per_serving(self) -> float:
        return self.__cost / self.__servings

    def profit(self) -> float:
        return self.__sale_price - self.__cost

    def to_dict(self) -> dict:
        return {'id': self.__id,
                'name': self.name,
                'servings': self.__servings,
                'serving_unit': self.serving_unit,
                'sale_price': self.__sale_price,
                'ingredients': [
                    {'amount': i.amount.magnitude,
                     'unit': f"{i.amount.units:~}",
                     'ingredient_id': i.ingredient.id
                     } for i in self.__ingredients],
                'cost': self.cost(),
                'cost_per_serving': self.cost_per_serving(),
                'profit': self.profit()}


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