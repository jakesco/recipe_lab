import unittest
from recipelab.ingredient import Ingredient


class TestIngredient(unittest.TestCase):
    def test_ingredient(self):
        x = Ingredient(1, "Test Ingredient", 10, 'oz', 20.00)
        print(x)

    def test_ingredient_custom_unit(self):
        x = Ingredient(2, "Test Ingredient", 10, 'cookie', 20.00)
        print(x)

    def test_ingredient_amount_less_than_equal_zero(self):
        x = Ingredient(1, "Test Ingredient", 10, 'oz', 20.00)
        print(x.cost_per_unit('cup'))

    def test_ingredient_cost_less_than_equal_zero(self):
        x = Ingredient(2, "Test Ingredient", 10, 'cookie', 20.00)
        with self.assertRaises(Exception):
            print(x.cost_per_unit('tsp'))

    def test_ingredient_amount_not_number(self):
        pass

    def test_ingredient_cost_not_number(self):
        pass

    def test_ingredient_price_per_unit(self):
        pass

    def test_ingredient_equality(self):
        pass

    def test_sets_same_ingredient(self):
        pass

    def test_sets_different_ingredient(self):
        pass

    def test_sets_remove_ingredient(self):
        pass


if __name__ == "__main__":
    unittest.main()
