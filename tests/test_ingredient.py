import unittest
from recipelab.ingredient import Ingredient


class TestIngredient(unittest.TestCase):
    def test_ingredient_dry(self):
        i = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
        self.assertEqual(i.unit, "oz")

    def test_ingredient_wet(self):
        i = Ingredient("test name", 10, 10, Ingredient.Type.FLUID)
        self.assertEqual(i.unit, "fl. oz")

    def test_ingredient_custom(self):
        i = Ingredient("test name", 10, 10, Ingredient.Type.OTHER, "cookie")
        self.assertEqual(i.unit, "cookie")

    def test_ingredient_amount_less_than_equal_zero(self):
        with self.assertRaises(Exception):
            Ingredient("test name", 10, 0, Ingredient.Type.DRY)
            Ingredient("test name", 10, -1, Ingredient.Type.DRY)

    def test_ingredient_cost_less_than_equal_zero(self):
        with self.assertRaises(Exception):
            Ingredient("test name", 10, -1, Ingredient.Type.DRY)
            Ingredient("test name", 10, 0, Ingredient.Type.DRY)

    def test_ingredient_amount_not_number(self):
        with self.assertRaises(Exception):
            Ingredient("test name", "hello", 10, Ingredient.Type.DRY)

    def test_ingredient_cost_not_number(self):
        with self.assertRaises(Exception):
            Ingredient("test name", 10, "cost", Ingredient.Type.DRY)

    def test_ingredient_price_per_unit(self):
        i = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
        self.assertEqual(i.cost_per_unit, 1)

    def test_ingredient_equality(self):
        i1 = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
        i2 = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
        i3 = Ingredient("test name", 10, 10, Ingredient.Type.FLUID)
        i4 = Ingredient("test name", 10, 10, Ingredient.Type.DRY, ingredient_id=1)
        i5 = Ingredient("Other Name", 10, 10, Ingredient.Type.DRY)
        i6 = Ingredient("test name", 10, 10, Ingredient.Type.OTHER, "cookie")
        self.assertEqual(i1, i2)
        self.assertNotEqual(i1, i3)
        self.assertEqual(i1, i4)
        self.assertNotEqual(i1, i5)
        self.assertNotEqual(i1, i6)

    def test_sets_same_ingredient(self):
        i1 = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
        i2 = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
        ingredients = set()
        ingredients.add(i1)
        ingredients.add(i2)
        self.assertEqual(ingredients, {i1})

    def test_sets_different_ingredient(self):
        i1 = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
        i2 = Ingredient("test name", 10, 10, Ingredient.Type.FLUID)
        ingredients = set()
        ingredients.add(i1)
        ingredients.add(i2)
        self.assertEqual(ingredients, {i1, i2})

    def test_sets_remove_ingredient(self):
        i1 = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
        i2 = Ingredient("test name", 10, 10, Ingredient.Type.FLUID)
        ingredients = {i1, i2}
        ingredients.remove(i1)
        self.assertEqual(ingredients, {i2})


if __name__ == "__main__":
    unittest.main()
