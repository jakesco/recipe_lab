class Recipe:
    def __init__(
        self, name, servings, serving_unit, sale_price, ingredients=[], id=None
    ):
        self.name = name
        self.servings = servings
        self.serving_unit = serving_unit
        self.sale_price = sale_price
        self.ingredients = ingredients
        self.id = id

    def __repr__(self):
        return f"Recipe({self.id} - {self.name}, {self.servings} {self.serving_unit}, ${self.sale_price:.2f}"
