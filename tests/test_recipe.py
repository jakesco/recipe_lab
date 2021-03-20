import unittest
from context import Recipe
from context import Ingredient


class Test(unittest.TestCase):
    def setUp(self):
        self.sample_ing = [
            Ingredient("Test Ing 1", 100, 100, Ingredient.Type.DRY),
            Ingredient("Test Ing 2", 100, 25, Ingredient.Type.FLUID),
            Ingredient("Test Ing 3", 100, 50, Ingredient.Type.OTHER, "tests"),
        ]

    def tearDown(self):
        # runs after each test
        pass

    def test_add_ingredient(self):
        r1 = Recipe("Test Recipe 1", 2, "plate", 25.50, [])
        r1.add_ingredient(20, self.sample_ing[0])
        self.assertEqual(len(r1.ingredients), 1)

    def test_add_same_ingredient(self):
        r1 = Recipe("Test Recipe 1", 2, "plate", 25.50, [])
        r1.add_ingredient(20, self.sample_ing[0])
        r1.add_ingredient(20, self.sample_ing[0])
        self.assertEqual(len(r1.ingredients), 1)

    def test_remove_ingredient(self):
        r1 = Recipe("Test Recipe 1", 2, "plate", 25.50, [])
        r1.add_ingredient(20, self.sample_ing[0])
        r1.remove_ingredient(20, self.sample_ing[0])
        self.assertEqual(len(r1.ingredients), 0)
        r1.add_ingredient(20, self.sample_ing[1])
        r1.add_ingredient(20, self.sample_ing[2])
        r1.remove_ingredient(20, self.sample_ing[2])
        self.assertEqual(len(r1.ingredients), 1)
        self.assertEqual(r1.ingredients[0].ingredient, self.sample_ing[1])

    def test_calcualte_cost(self):
        r1 = Recipe("Test Recipe 1", 2, "plate", 25.50, [])
        self.assertEqual(r1.cost(), 0)
        r1.add_ingredient(20, self.sample_ing[0])
        self.assertEqual(r1.cost(), 20)
        r1.add_ingredient(4, self.sample_ing[1])
        self.assertEqual(r1.cost(), 21)
        r1.add_ingredient(2, self.sample_ing[2])
        self.assertEqual(r1.cost(), 22)

    def test_cost_per_serving(self):
        r1 = Recipe("Test Recipe 1", 2, "plate", 25.50, [])
        self.assertEqual(r1.cost_per_serving(), 0)
        r1.add_ingredient(20, self.sample_ing[0])
        self.assertEqual(r1.cost_per_serving(), 10)
        r1.add_ingredient(4, self.sample_ing[1])
        self.assertEqual(r1.cost_per_serving(), 10.5)
        r1.add_ingredient(2, self.sample_ing[2])
        self.assertEqual(r1.cost_per_serving(), 11)

    def test_profit(self):
        r1 = Recipe("Test Recipe 1", 2, "plate", 25, [])
        self.assertEqual(r1.profit(), 25)
        r1.add_ingredient(20, self.sample_ing[0])
        self.assertEqual(r1.profit(), 5)
        r1.add_ingredient(4, self.sample_ing[1])
        self.assertEqual(r1.profit(), 4)
        r1.add_ingredient(2, self.sample_ing[2])
        self.assertEqual(r1.profit(), 3)


if __name__ == "__main__":
    unittest.main()