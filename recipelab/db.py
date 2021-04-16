import sqlite3
import os
from recipelab import log

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class DB:
    def __init__(self, db_path: str):
        self._db_conn = sqlite3.connect(db_path)
        self._db_conn.row_factory = sqlite3.Row
        self._db_cur = self._db_conn.cursor()

        # Check if db needs to be initialized
        self._db_cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table'")
        if self._db_cur.fetchone()['count(name)'] == 0:
            #log.info("Initializing DB.")
            self.init_db()

    def __del__(self):
        self._db_conn.close()

    def init_db(self):
        with open(os.path.join(__location__, "schema.sql")) as f:
            self._db_cur.executescript(f.read())

    # Create
    def insert_ingredient(self, name: str, amount: float, unit: str, cost: float):
        with self._db_conn:
            self._db_cur.execute(
                "INSERT INTO ingredient VALUES (?, ?, ?, ?, ?)",
                (None, name, amount, unit, cost),
            )

        # Get assigned id
        self._db_cur.execute("SELECT id FROM ingredient WHERE name = :name", {"name": name})
        ingredient_id = self._db_cur.fetchone()['id']

        log.info(f"Ingredient ({ingredient_id} - {name}) added to database.")
        return ingredient_id

    def insert_recipe_ingredient(self, recipe_id: int, ingredient_id: int, amount: float, unit: str):
        with self._db_conn:
            self._db_cur.execute(
                "INSERT INTO recipe_ingredient VALUES (?, ?, ?, ?)",
                (recipe_id, ingredient_id, amount, unit),
            )

    def insert_recipe(self,
                      name: str,
                      servings: float,
                      sale_price: float,
                      serving_unit: str = None,
                      ingredients_list: list[tuple[int, float, str]] = None):
        with self._db_conn:
            self._db_cur.execute(
                "INSERT INTO recipe VALUES (?, ?, ?, ?, ?)",
                (None, name, servings, serving_unit, sale_price),
            )

        # Get assigned id
        self._db_cur.execute("SELECT id FROM recipe WHERE name = :name", {"name": name})
        recipe_id = self._db_cur.fetchone()['id']

        if ingredients_list is not None:
            for ingredient_id, amount, unit in ingredients_list:
                self.insert_recipe_ingredient(recipe_id, ingredient_id, amount, unit)

        log.info(f"Ingredient ({recipe_id} - {name}) added to database.")
        return recipe_id

    # Retrieve
    def get_ingredients(self, ids: tuple[int, ...]) -> list[dict]:
        sql = 'SELECT * FROM ingredient WHERE id IN (%s)' % ', '.join('?' for _ in ids)
        self._db_cur.execute(sql, ids)
        return [dict(i) for i in self._db_cur.fetchall()]

    def get_all_ingredients(self) -> list[dict]:
        self._db_cur.execute("SELECT * FROM ingredient")
        return [dict(i) for i in self._db_cur.fetchall()]

    def get_ingredients_for_recipe(self, recipe_id: int) -> list[dict]:
        self._db_cur.execute("SELECT ingredient_id as id, amount, unit FROM recipe_ingredient WHERE recipe_id = ?", (recipe_id,))
        return [dict(ri) for ri in self._db_cur.fetchall()]

    def get_recipes(self, ids: tuple[int, ...]) -> list[dict]:
        sql = 'SELECT * FROM recipe WHERE id IN (%s)' % ', '.join('?' for _ in ids)
        self._db_cur.execute(sql, ids)
        recipes = [dict(r) for r in self._db_cur.fetchall()]
        for r in recipes:
            r['ingredients'] = self.get_ingredients_for_recipe(r['id'])
        return recipes

    def get_all_recipes(self) -> list[dict]:
        self._db_cur.execute("SELECT * FROM recipe")
        recipes = [dict(r) for r in self._db_cur.fetchall()]
        for r in recipes:
            r['ingredients'] = self.get_ingredients_for_recipe(r['id'])
        return recipes

    # TODO: Update

    # Delete
    def delete_ingredients(self, ids: tuple[int, ...]):
        with self._db_conn:
            for i in ids:
                self._db_cur.execute(
                    "DELETE FROM recipe_ingredient WHERE ingredient_id = ?", (i,)
                )
                self._db_cur.execute("DELETE FROM ingredient WHERE id = ?", (i,))
        log.info(f"Ingredient id({id}) removed from database.")

    def delete_recipes(self, ids: tuple[int, ...]):
        with self._db_conn:
            for r in ids:
                self._db_cur.execute(
                    "DELETE FROM recipe_ingredient WHERE recipe_id = ?", (r,)
                )
                self._db_cur.execute("DELETE FROM recipe WHERE id = ?", (r,))
        log.info(f"Recipe id({id}) removed from database.")
