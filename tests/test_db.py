import unittest
from context import DB


class TestCore(unittest.TestCase):
    def setUp(self):
        self.db = DB(":memory:")
        self.db.init_db()

        with open("tests/sample_data.sql") as f:
            self.db._db_cur.executescript(f.read())

    def test_get_ingredient(self):
        i1 = self.db.get_ingredient(1)
        cmp1 = {
            "id": 1,
            "name": "Unsalted Crackers",
            "amount_per_unit": 140,
            "price_per_unit": 1.23,
            "type": 3,
            "unit": "cracker",
        }

        for k, v in cmp1.items():
            self.assertEqual(i1[k], v)

    def test_get_ingredient_by_name(self):
        i1 = self.db.get_ingredient_by_name("Unsalted Crackers")
        cmp1 = {
            "id": 1,
            "name": "Unsalted Crackers",
            "amount_per_unit": 140,
            "price_per_unit": 1.23,
            "type": 3,
            "unit": "cracker",
        }

        for k, v in cmp1.items():
            self.assertEqual(i1[k], v)

    def test_get_all_ingredients(self):
        i = self.db.get_all_ingredients()
        self.assertEqual(len(i), 6)

    def test_get_recipe(self):
        i1 = self.db.get_recipe(1)
        cmp1 = {
            "id": 1,
            "name": "Chocolate Caramel Toffee",
            "servings": 24,
            "serving_unit": "cracker",
            "sale_price": 20,
        }

        for k, v in cmp1.items():
            self.assertEqual(i1[k], v)

    def test_get_recipe_by_name(self):
        i1 = self.db.get_recipe_by_name("Chocolate Caramel Toffee")
        cmp1 = {
            "id": 1,
            "name": "Chocolate Caramel Toffee",
            "servings": 24,
            "serving_unit": "cracker",
            "sale_price": 20,
        }

        for k, v in cmp1.items():
            self.assertEqual(i1[k], v)

    def test_get_all_recipes(self):
        i = self.db.get_all_recipes()
        self.assertEqual(len(i), 1)

    def test_get_ingredients_for_recipe(self):
        r = self.db.get_ingredients_for_recipe(1)
        self.assertEqual(len(r), 6)


if __name__ == "__main__":
    unittest.main()
