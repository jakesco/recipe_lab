import unittest
from context import RecipeLab
from pprint import pprint


class Test(unittest.TestCase):
    def setUp(self):
        self.rl = RecipeLab(":memory:")
        with open("tests/sample_data.sql") as f:
            self.rl.db._db_cur.executescript(f.read())

    def test_list_ingredients(self):
        pass

    def test_get_recipe(self):
        pass

    def test_list_recipes(self):
        pprint(self.rl.list_recipes())

    def test_fuzzy_name_search(self):
        ing = self.rl.list_ingredients()
        pprint(ing)
        print()
        ing_s = self.rl.fuzzy_name_search("s", ing)
        pprint(ing_s)
        print()
        rec = self.rl.list_recipes()
        pprint(rec)
        print()
        rec_s = self.rl.fuzzy_name_search("Toffee", rec)
        pprint(rec_s)
        print()


if __name__ == "__main__":
    unittest.main()
