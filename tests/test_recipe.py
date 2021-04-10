import unittest
from recipelab.ingredient import Ingredient
from recipelab.recipe import Recipe, IngredientAmount


class TestRecipe(unittest.TestCase):
    def test_no_ingredients(self):
        r = Recipe("test recipe", 10, 1, 10)
        self.assertEqual(r.__ingredients, [])

    def test_with_ingredients_list(self):
        i1 = Ingredient("test ingredient 1", 10, 10, Ingredient.Type.DRY)
        i2 = Ingredient("test ingredient 2", 10, 10, Ingredient.Type.DRY)
        ingredient_list = [IngredientAmount(10, i1), IngredientAmount(20, i2)]
        r = Recipe("test recipe", 10, 1, 10, ingredient_list)
        self.assertEqual(r.__ingredients, ingredient_list)

    def test_with_bad_ingredients_list(self):
        with self.assertRaises(Exception):
            i1 = Ingredient("test ingredient 1", 10, 10, Ingredient.Type.DRY)
            i2 = Ingredient("test ingredient 2", 10, 10, Ingredient.Type.DRY)
            ingredient_list = [i1, i2]
            Recipe("test recipe", 10, 1, 10, ingredient_list)

    def test_servings_less_equal_zero(self):
        with self.assertRaises(Exception):
            Recipe("test recipe", 0, "plates", 1)
            Recipe("test recipe", -1, "plates", 1)

    def test_servings_not_a_number(self):
        with self.assertRaises(Exception):
            Recipe("test recipe", "not a number", "plates", 1)

    def test_sale_price_less_equal_zero(self):
        with self.assertRaises(Exception):
            Recipe("test recipe", 1, "plates", 0)
            Recipe("test recipe", 1, "plates", -1)

    def test_sale_price_not_a_number(self):
        with self.assertRaises(Exception):
            Recipe("test recipe", 1, "plates", "not a number")

    def test_add_ingredient(self):
        r = Recipe("test recipe", 1, "plate", 20.00)
        i = Ingredient("Test Ingredient", 1, 1, Ingredient.Type.DRY)
        r.add_ingredient(10, i)
        self.assertIsInstance(r.__ingredients[0], IngredientAmount)
        self.assertEqual(r.__ingredients[0].ingredient, i)
        self.assertEqual(r.__ingredients[0].amount, 10)

    def test_add_same_ingredient(self):
        r = Recipe("test recipe", 1, "plate", 20.00)
        i1 = Ingredient("Test Ingredient", 1, 1, Ingredient.Type.DRY)
        i2 = Ingredient("Test Ingredient", 1, 1, Ingredient.Type.DRY)
        r.add_ingredient(10, i1)
        r.add_ingredient(10, i2)
        self.assertEqual(len(r.__ingredients), 1)

    def test_remove_ingredient(self):
        i1 = Ingredient("Test Ingredient", 1, 1, Ingredient.Type.DRY)
        i2 = Ingredient("Test Ingredient", 1, 1, Ingredient.Type.DRY)
        r = Recipe("test recipe", 1, "plate", 20.00, [IngredientAmount(10, i1), IngredientAmount(20, i2)])
        r.remove_ingredient(10, i1)
        self.assertEqual(r.__ingredients[0].ingredient, i2)
        self.assertEqual(r.__ingredients[0].amount, 20)

    def test_cost(self):
        i1 = Ingredient("Test Ingredient", 1, 1, Ingredient.Type.DRY)
        i2 = Ingredient("Test Ingredient", 1, 1, Ingredient.Type.DRY)
        r1 = Recipe("test recipe", 1, "plate", 20.00)
        r2 = Recipe("test recipe", 1, "plate", 20.00, [IngredientAmount(10, i1)])
        r3 = Recipe("test recipe", 1, "plate", 20.00, [IngredientAmount(10, i1), IngredientAmount(20, i2)])
        self.assertEqual(r1.cost(), 0)
        self.assertEqual(r2.cost(), 10)
        self.assertEqual(r3.cost(), 30)

    def test_cost_per_serving(self):
        i1 = Ingredient("Test Ingredient", 1, 1, Ingredient.Type.DRY)
        i2 = Ingredient("Test Ingredient", 1, 1, Ingredient.Type.DRY)
        r1 = Recipe("test recipe", 2, "plate", 20.00)
        r2 = Recipe("test recipe", 2, "plate", 20.00, [IngredientAmount(10, i1)])
        r3 = Recipe("test recipe", 2, "plate", 20.00, [IngredientAmount(10, i1), IngredientAmount(20, i2)])
        self.assertEqual(r1.cost_per_serving(), 0)
        self.assertEqual(r2.cost_per_serving(), 5)
        self.assertEqual(r3.cost_per_serving(), 15)

    def test_profit(self):
        i1 = Ingredient("Test Ingredient", 1, 1, Ingredient.Type.DRY)
        i2 = Ingredient("Test Ingredient", 1, 1, Ingredient.Type.DRY)
        r1 = Recipe("test recipe", 1, "plate", 20.00)
        r2 = Recipe("test recipe", 1, "plate", 20.00, [IngredientAmount(10, i1)])
        r3 = Recipe("test recipe", 1, "plate", 20.00, [IngredientAmount(10, i1), IngredientAmount(20, i2)])
        self.assertEqual(r1.profit(), 20)
        self.assertEqual(r2.profit(), 10)
        self.assertEqual(r3.profit(), -10)

    def test_equality(self):
        r1 = Recipe("test recipe", 1, "plate", 20.00)
        r2 = Recipe("test recipe", 1, "plate", 20.00)
        self.assertEqual(r1, r2)

        i1 = Ingredient("Test Ingredient", 1, 1, Ingredient.Type.DRY)
        i2 = Ingredient("Test Ingredient", 1, 1, Ingredient.Type.DRY)
        r3 = Recipe("test recipe", 1, "plate", 20.00, [IngredientAmount(10, i1), IngredientAmount(20, i2)])
        r4 = Recipe("test recipe", 1, "plate", 20.00, [IngredientAmount(10, i1), IngredientAmount(20, i2)])
        self.assertEqual(r3, r4)

    def test_sets_same_recipe(self):
        i1 = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
        i2 = Ingredient("test name", 10, 10, Ingredient.Type.FLUID)
        r1 = Recipe("test recipe", 1, "plate", 20.00, [IngredientAmount(10, i1), IngredientAmount(20, i2)])
        r2 = Recipe("test recipe", 1, "plate", 20.00, [IngredientAmount(10, i1), IngredientAmount(20, i2)])
        recipes = set()
        recipes.add(r1)
        recipes.add(r2)
        self.assertEqual(recipes, {r1})

    def test_sets_different_recipe(self):
        i1 = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
        i2 = Ingredient("test name", 10, 10, Ingredient.Type.FLUID)
        r1 = Recipe("test recipe", 1, "plate", 20.00, [IngredientAmount(10, i1), IngredientAmount(20, i2)])
        r2 = Recipe("test recipe", 1, "plate", 20.00,)
        recipes = set()
        recipes.add(r1)
        recipes.add(r2)
        self.assertEqual(recipes, {r1, r2})

    def test_sets_remove_recipe(self):
        i1 = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
        i2 = Ingredient("test name", 10, 10, Ingredient.Type.FLUID)
        r1 = Recipe("test recipe", 1, "plate", 20.00, [IngredientAmount(10, i1), IngredientAmount(20, i2)])
        r2 = Recipe("test recipe", 1, "plate", 20.00,)
        recipes = {r1, r2}
        recipes.remove(r1)
        self.assertEqual(recipes, {r2})


if __name__ == "__main__":
    unittest.main()