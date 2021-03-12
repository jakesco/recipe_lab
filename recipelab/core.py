def ingredient_cost(db, ingredient_id, amount):
    ingredient = db.get_ingredient(ingredient_id)
    return round((ingredient.price_per_unit * amount) / ingredient.amount_per_unit, 2)


def recipe_cost(db, recipe):
    costs = map(lambda x: ingredient_cost(db, x[0], x[1]), recipe.ingredients)
    return sum(costs)


def cost_per_serving(db, recipe):
    return round(recipe_cost(db, recipe) / recipe.servings, 2)


def net_gain(db, recipe):
    return round(recipe.sale_price - recipe_cost(db, recipe), 2)
