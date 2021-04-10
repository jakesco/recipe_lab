import unittest
import json
from recipelab.ingredient import Ingredient
from recipelab.recipe import Recipe, RecipeIngredient


class TestRecipe(unittest.TestCase):
    def test_recipe(self):
        r = Recipe(1, "Test Recipe", 1, 'plate', 20.0)
        print(r)
        print(r.to_dict())

    def test_recipe_with_ingredients(self):
        i1 = Ingredient(1, "Test Ingredient 1", 1, 'tsp', .5)
        i2 = Ingredient(2, "Test Ingredient 2", 1, 'cup', 2)
        r = Recipe(1, "Test Recipe", 1, 'plate', 20.0)
        r.add_ingredient(1, 'tbsp', i1)
        r.add_ingredient(1, 'cup', i2)
        print(r)
        print(r.to_dict())
        print(json.dumps(r.to_dict(), indent=2))


if __name__ == "__main__":
    unittest.main()