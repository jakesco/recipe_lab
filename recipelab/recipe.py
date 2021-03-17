class Recipe:
    def __init__(
        self, name, servings, serving_unit, sale_price, ingredients=[], id=None
    ):
        self.name = name
        self.servings = servings
        self.serving_unit = serving_unit
        self.sale_price = sale_price
        # the ingredients are tuples with (amount(float), Ingredient(object))
        self.ingredients = ingredients
        self.id = id

    def __repr__(self):
        return "Recipe({} - {}, {} {}, ${:.2f}, {} ingredients)".format(
            self.id,
            self.name,
            self.servings,
            self.serving_unit,
            self.sale_price,
            len(self.ingredients),
        )

    def cost(self):
        costs = map(lambda x: x[1].cost(x[0]), self.ingredients)
        return sum(costs)

    def cost_per_serving(self):
        return round(self.cost() / self.servings, 2)

    def profit(self):
        return round(self.sale_price - self.cost(), 2)
