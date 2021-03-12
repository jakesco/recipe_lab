import unittest
from recipelab.db import DB
from recipelab.objects import Recipe, Ingredient
from recipelab.core import ingredient_cost, recipe_cost, cost_per_serving, net_gain


class TestCore(unittest.TestCase):
    def setUp(self):
        self.db = DB(":memory:")
        self.db.init_db()

        ingredients = [
            Ingredient(
                "Unsalted Crackers", 140, 1.23, Ingredient.Type.OTHER, "cracker"
            ),
            Ingredient("Unsalted Butter", 16, 2.94, Ingredient.Type.DRY),
            Ingredient("Brown Sugar", 32, 2.73, Ingredient.Type.DRY),
            Ingredient("Salt", 4.4, 0.98, Ingredient.Type.DRY),
            Ingredient("Vanilla Extract", 2, 4.98, Ingredient.Type.FLUID),
            Ingredient("Semi-Sweet Chocolate Chips", 12, 1.74, Ingredient.Type.DRY),
        ]

        for i in ingredients:
            self.db.insert_ingredient(i)

        recipe = Recipe(
            "Chocolate Caramel Toffee",
            24,
            "crackers",
            20.00,
            [(1, 40), (2, 8), (3, 8), (4, 0.05), (5, 0.87), (6, 12)],
        )

        self.db.insert_recipe(recipe)

    def tearDown(self):
        # runs after each test
        pass

    @classmethod
    def setUpClass(cls):
        # Runs once before any tests
        pass

    @classmethod
    def tearDownClass(cls):
        # Runs once after all tests
        pass

    def test_ingredient_cost(self):
        self.assertAlmostEqual(ingredient_cost(self.db, 1, 40), 0.35)

    def test_recipe_cost(self):
        recipe = self.db.get_recipe(1)
        self.assertAlmostEqual(recipe_cost(self.db, recipe), 6.42)

    def test_cost_per_serving(self):
        recipe = self.db.get_recipe(1)
        self.assertAlmostEqual(cost_per_serving(self.db, recipe), 0.27)

    def test_net_gain(self):
        recipe = self.db.get_recipe(1)
        self.assertAlmostEqual(net_gain(self.db, recipe), 13.58)


if __name__ == "__main__":
    unittest.main()
