import unittest
import context
import sqlite3
from recipelab.db import DB


class TestCore(unittest.TestCase):
    def setUp(self):
        self.db = DB(":memory:")

        with open("./sample_data.sql") as f:
            self.db._db_cur.executescript(f.read())

    def test_insert_ingredient(self):
        self.db._db_cur.execute("SELECT max(id) FROM Ingredient")
        next_id = int(self.db._db_cur.fetchone()['max(id)']) + 1

        i_id = self.db.insert_ingredient("Test Ingredient", 10, "tsp", 20)
        self.db._db_cur.execute('SELECT * FROM Ingredient WHERE name = "Test Ingredient"')
        result = dict(self.db._db_cur.fetchone())

        self.assertEqual(i_id, next_id)
        self.assertEqual(result, {'id': next_id, 'name': 'Test Ingredient', 'amount': 10.0, 'unit': 'tsp', 'cost': 20.0})

    def test_insert_ingredient_same_name(self):
        self.db._db_cur.execute('INSERT INTO Ingredient VALUES (100, "Test Ingredient", 11, "tbp", 10)')
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.insert_ingredient("Test Ingredient", 10, "tsp", 20)

    def test_insert_ingredient_null_values(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.insert_ingredient(None, 10, "tsp", 20)
            self.db.insert_ingredient("Test Ingredient", None, "tsp", 20)
            self.db.insert_ingredient("Test Ingredient", 10, None, 20)
            self.db.insert_ingredient("Test Ingredient", 10, "tsp", None)

    def test_insert_recipe_ingredient(self):
        self.db._db_cur.execute('INSERT INTO ingredient VALUES (100, "Test Ingredient", 11, "tbp", 10)')
        self.db._db_cur.execute('INSERT INTO recipe VALUES (100, "Test Recipe", 11, "plate", 10)')
        self.db.insert_recipe_ingredient(100, 100, 10, 'tsp')
        self.db._db_cur.execute('SELECT * FROM recipe_ingredient WHERE recipe_id = 100')
        result = dict(self.db._db_cur.fetchone())
        self.assertEqual(result, {'recipe_id': 100, 'ingredient_id': 100, 'amount': 10.0, 'unit': 'tsp'})

    def test_insert_recipe_ingredient_same_key(self):
        self.db._db_cur.execute('INSERT INTO ingredient VALUES (100, "Test Ingredient", 11, "tbp", 10)')
        self.db._db_cur.execute('INSERT INTO recipe VALUES (100, "Test Recipe", 11, "plate", 10)')
        self.db._db_cur.execute('INSERT INTO recipe_ingredient VALUES (100, 100, 11, "cup")')
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.insert_recipe_ingredient(100, 100, 10, 'tsp')

    def test_insert_recipe_ingredient_no_recipe(self):
        self.db._db_cur.execute('INSERT INTO ingredient VALUES (100, "Test Ingredient", 11, "tbp", 10)')
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.insert_recipe_ingredient(100, 100, 10, 'tsp')

    def test_insert_recipe_ingredient_no_ingredient(self):
        self.db._db_cur.execute('INSERT INTO recipe VALUES (100, "Test Recipe", 11, "plate", 10)')
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.insert_recipe_ingredient(100, 100, 10, 'tsp')

    def test_insert_recipe_no_unit_no_ingredients(self):
        self.db._db_cur.execute("SELECT max(id) FROM recipe")
        next_id = int(self.db._db_cur.fetchone()['max(id)']) + 1

        r_id = self.db.insert_recipe("Test Recipe", 10, 20)
        self.db._db_cur.execute('SELECT * FROM recipe WHERE name = "Test Recipe"')
        result = dict(self.db._db_cur.fetchone())

        self.assertEqual(r_id, next_id)
        self.assertEqual(result, {'id': next_id, 'name': 'Test Recipe', 'servings': 10.0, 'serving_unit': None, 'sale_price': 20.0})

    def test_get_ingredients(self):
        result = self.db.get_ingredients((1, 8, 20))
        self.assertEqual(result,
                         [{'id': 1, 'name': 'Unsalted Crackers', 'amount': 140.0, 'unit': 'cracker', 'cost': 1.23},
                          {'id': 8, 'name': 'Yeast', 'amount': 2.25, 'unit': 'tsp', 'cost': 0.8}]
                         )

    def test_get_ingredients_for_recipe(self):
        result = self.db.get_ingredients_for_recipe(1)
        self.assertEqual(result, [{'id': 1, 'amount': 40.0, 'unit': 'cracker'}, {'id': 2, 'amount': 8.0, 'unit': 'oz'},
         {'id': 3, 'amount': 8.0, 'unit': 'oz'}, {'id': 4, 'amount': 0.25, 'unit': 'tsp'},
         {'id': 5, 'amount': 0.5, 'unit': 'tsp'}, {'id': 6, 'amount': 11.0, 'unit': 'oz'}]
        )

    def test_get_recipes(self):
        result = self.db.get_recipes((1,))
        self.assertEqual(result, [{'id': 1, 'name': 'Chocolate Caramel Toffee', 'servings': 24.0, 'serving_unit': None, 'sale_price': 20.0,
          'ingredients': [{'id': 1, 'amount': 40.0, 'unit': 'cracker'}, {'id': 2, 'amount': 8.0, 'unit': 'oz'},
                          {'id': 3, 'amount': 8.0, 'unit': 'oz'}, {'id': 4, 'amount': 0.25, 'unit': 'tsp'},
                          {'id': 5, 'amount': 0.5, 'unit': 'tsp'}, {'id': 6, 'amount': 11.0, 'unit': 'oz'}]}]
        )

if __name__ == "__main__":
    unittest.main()
