import unittest
from pprint import pprint
from context import Ingredient
from context import RecipeLab


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Testing RecipeLab")

    def setUp(self):
        self.rl = RecipeLab(":memory:")
        with open("tests/sample_data.sql") as f:
            self.rl.db._db_cur.executescript(f.read())

    def test_new_ingredient(self):
        pass

    def test_new_recipe(self):
        pass

    def test_add_ingredient_to_recipe(self):
        pass

    def test_list_ingredients(self):
        pprint(self.rl.list_ingredients())


if __name__ == "__main__":
    unittest.main()
