import unittest
import context
from recipelab.api import success, failed, RecipeLabAPI


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.api = RecipeLabAPI()
        with open("./sample_data.sql") as f:
            self.api.repo._db._db_cur.executescript(f.read())
        self.api.repo.refresh()

    def test_all_ingredients(self):
        result = self.api.all_ingredients()

    def test_all_recipes(self):
        result = self.api.all_recipes()

    def test_get_ingredients(self):
        result = self.api.get_ingredients('{"ids":[1,2,3,4]}')

    def test_get_recipes(self):
        result = self.api.get_recipes('{"ids":[1,2]}')
        print(result)

    def test_new_ingredient(self):
        result = self.api.new_ingredient('{"name": "test", "amount": null, "unit": null, "cost": null}')
        print(result)


if __name__ == "__main__":
    unittest.main()
