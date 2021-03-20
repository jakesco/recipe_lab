from collections import namedtuple


IngredientAmount = namedtuple("IngredientAmount", "amount, ingredient")


class Recipe:
    def __init__(self, name, servings, serving_unit, sale_price, ingredients):
        self.name = name
        self.servings = servings
        self.serving_unit = serving_unit
        self.sale_price = sale_price
        # the ingredients are IngredientAmount named tuples
        self.ingredients = ingredients

    def __repr__(self):
        return "Recipe({}, {} {}, ${:.2f}, {} ingredients)".format(
            self.name,
            self.servings,
            self.serving_unit,
            self.sale_price,
            len(self.ingredients),
        )

    def add_ingredient(self, amount, ingredient):
        ingredient_amount = IngredientAmount(amount, ingredient)
        if ingredient_amount not in self.ingredients:
            self.ingredients.append(ingredient_amount)

    def remove_ingredient(self, amount, ingredient):
        ingredient_amount = IngredientAmount(amount, ingredient)
        ingredients = filter(lambda x: ingredient_amount != x, self.ingredients)
        self.ingredients = list(ingredients)

    def cost(self):
        costs = map(lambda x: x.amount * x.ingredient.cost_per_unit, self.ingredients)
        return sum(costs)

    def cost_per_serving(self):
        return self.cost() / self.servings

    def profit(self):
        return self.sale_price - self.cost()
