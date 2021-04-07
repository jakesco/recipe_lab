from collections import namedtuple

IngredientAmount = namedtuple("IngredientAmount", "amount, ingredient")


class Recipe:
    def __init__(self, name, servings, serving_unit, sale_price, ingredients_list=None, recipe_id=None):
        self.id = recipe_id
        self.name = name

        try:
            self.servings = float(servings)
        except ValueError:
            raise Exception("Servings must be a number.")

        if self.servings <= 0:
            raise Exception("Servings must be greater than 0.")

        self.serving_unit = serving_unit

        try:
            self.sale_price = float(sale_price)
        except ValueError:
            raise Exception("Sale price must be a number.")

        if self.sale_price <= 0:
            raise Exception("Sale price must be greater than 0.")

        # the ingredients are IngredientAmount named tuples
        if ingredients_list is None:
            self.ingredients = []
        else:
            if False in [isinstance(i, IngredientAmount) for i in ingredients_list]:
                raise Exception("Ingredient list must be of type [IngredientAmount]")
            self.ingredients = ingredients_list

    def __repr__(self):
        return "Recipe({} - {}, {} {}, ${:.2f}, {} ingredients)".format(
            self.id,
            self.name,
            self.servings,
            self.serving_unit,
            self.sale_price,
            len(self.ingredients)
        )

    def __hash__(self):
        return hash((self.name, self.servings, self.serving_unit, self.sale_price, len(self.ingredients)))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (self.name == other.name
                and self.servings == other.servings
                and self.serving_unit == other.serving_unit
                and self.sale_price == other.sale_price
                and self.ingredients == other.ingredients)

    def add_ingredient(self, amount, ingredient):
        ingredient_amount = IngredientAmount(amount, ingredient)
        if ingredient_amount not in self.ingredients:
            self.ingredients.append(ingredient_amount)

    def remove_ingredient(self, amount, ingredient):
        ingredient_amount = IngredientAmount(amount, ingredient)
        self.ingredients = [i for i in self.ingredients if i != ingredient_amount]

    def cost(self):
        return sum([i.amount * i.ingredient.cost_per_unit for i in self.ingredients])

    def cost_per_serving(self):
        return self.cost() / self.servings

    def profit(self):
        return self.sale_price - self.cost()
