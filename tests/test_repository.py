import unittest
from recipelab.repository import Repository, Ingredient, Recipe


class TestRepository(unittest.TestCase):

    def test_add_ingredient(self):
        repo = Repository()
        i = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
        repo.add(i)
        self.assertEqual(repo._ingredients, {i})

    def test_add_recipe(self):
        repo = Repository()
        r = Recipe("test recipe", 1, "plate", 20.00,)
        repo.add(r)
        self.assertEqual(repo._recipes, {r})

    def test_add_invalid_item(self):
        repo = Repository()
        x = 10
        with self.assertRaises(Exception):
            repo.add(x)

    def test_delete_ingredient(self):
        repo = Repository()
        i1 = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
        i2 = Ingredient("test name", 10, 10, Ingredient.Type.FLUID)
        repo._ingredients = {i1, i2}
        repo.remove(i1)
        self.assertEqual(repo._ingredients, {i2})

    def test_delete_recipe(self):
        repo = Repository()
        r1 = Recipe("test recipe1", 1, "plate", 20.00)
        r2 = Recipe("test recipe2", 1, "plate", 20.00)
        repo._recipes = {r1, r2}
        repo.remove(r1)
        self.assertEqual(repo._recipes, {r2})

    def test_delete_invalid_item(self):
        repo = Repository()
        r1 = Recipe("test recipe1", 1, "plate", 20.00)
        r2 = Recipe("test recipe2", 1, "plate", 20.00)
        repo._ingredients = {r1, r2}
        x = 10
        with self.assertRaises(Exception):
            repo.remove(x)
        self.assertEqual(repo._ingredients, {r1, r2})

    def test_list_ingredients(self):
        repo = Repository()
        i1 = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
        i2 = Ingredient("test name", 10, 10, Ingredient.Type.FLUID)
        repo._ingredients = {i1, i2}
        self.assertEqual(repo.list_ingredients(), {i1, i2})

    def test_list_recipes(self):
        repo = Repository()
        r1 = Recipe("test recipe1", 1, "plate", 20.00)
        r2 = Recipe("test recipe2", 1, "plate", 20.00)
        repo._recipes = {r1, r2}
        self.assertEqual(repo.list_recipes(), {r1, r2})

    def test_db_load(self):
        repo = Repository()
        repo._db.init_db()

        with open("./sample_data.sql") as f:
            repo._db._db_cur.executescript(f.read())

        repo._load_data()
        print(repo._ingredients)
        print(repo._recipes)


if __name__ == "__main__":
    unittest.main()
#    i1 = Ingredient("test name", 10, 10, Ingredient.Type.DRY)
#    i2 = Ingredient("test name", 10, 10, Ingredient.Type.FLUID)
#    r1 = Recipe("test recipe", 1, "plate", 20.00, [IngredientAmount(10, i1), IngredientAmount(20, i2)])
#    r2 = Recipe("test recipe", 1, "plate", 20.00, [IngredientAmount(10, i1), IngredientAmount(20, i2)])
