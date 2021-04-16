import unittest
import context
from recipelab.api import success, failed, RecipeLabAPI


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.api = RecipeLabAPI()
        with open("./sample_data.sql") as f:
            self.api.repo._db._db_cur.executescript(f.read())
        self.api.repo.refresh()

    def test_failed(self):
        message = "test fail"
        print(failed(message, indent=2))

    def test_success(self):
        message = {1: "this", 2: "is", 3: "a", 4: "test"}
        print(success(message, indent=2))

    def test_all_ingredients(self):
        result = self.api.all_ingredients()
        print(result)

    def test_all_recipes(self):
        result = self.api.all_recipes()
        print(result)

    def test_get_ingredients(self):
        result = self.api.get_ingredients((1,))
        print(result)

    def test_get_recipes(self):
        result = self.api.get_recipes((1,))
        print(result)


if __name__ == "__main__":
    unittest.main()
