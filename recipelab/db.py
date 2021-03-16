import sqlite3
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class DB(object):
    def __init__(self, db_path):
        self._db_conn = sqlite3.connect(db_path)
        self._db_conn.row_factory = sqlite3.Row
        self._db_cur = self._db_conn.cursor()

    def __del__(self):
        self._db_conn.close()

    def init_db(self):
        with open(os.path.join(__location__, "schema.sql")) as f:
            self._db_cur.executescript(f.read())

    # Create
    def insert_ingredient(
        self, name, amount_per_unit, price_per_unit, type_value, unit
    ):
        with self._db_conn:
            self._db_cur.execute(
                "INSERT INTO ingredient VALUES (?, ?, ?, ?, ?, ?)",
                (None, name, amount_per_unit, price_per_unit, type_value, unit),
            )

    def insert_recipe_ingredient(self, recipe_id, ingredient_id, amount):
        with self._db_conn:
            self._db_cur.execute(
                "INSERT INTO recipe_ingredient VALUES (?, ?, ?)",
                (recipe_id, ingredient_id, amount),
            )

    def insert_recipe(self, name, servings, serving_unit, sale_price, ingredients):
        with self._db_conn:
            self._db_cur.execute(
                "INSERT INTO recipe VALUES (?, ?, ?, ?, ?)",
                (None, name, servings, serving_unit, sale_price),
            )

        # Database may assign a different id, this ensures we have the correct id
        self._db_cur.execute("SELECT id FROM recipe WHERE name = :name", {"name": name})
        recipe_id = self._db_cur.fetchone()[0]

        for amount, ingredient in ingredients:
            self.insert_recipe_ingredients(recipe_id, ingredient.id, amount)

    # Retrieve
    def get_ingredient(self, id):
        self._db_cur.execute("SELECT * FROM ingredient WHERE id = ?", (str(id)))
        return self._db_cur.fetchone()

    def get_ingredient_by_name(self, name):
        self._db_cur.execute(
            "SELECT * FROM ingredient WHERE name = :name", {"name": name}
        )
        return self._db_cur.fetchone()

    def get_all_ingredients(self):
        self._db_cur.execute("SELECT * FROM ingredient")
        return self._db_cur.fetchall()

    def get_ingredients_for_recipe(self, recipe_id):
        self._db_cur.execute(
            "SELECT * FROM recipe_ingredient WHERE recipe_id = ?", (str(recipe_id))
        )
        return self._db_cur.fetchall()

    def get_recipe(self, id):
        self._db_cur.execute("SELECT * FROM recipe WHERE id = ?", (str(id)))
        return self._db_cur.fetchone()

    def get_recipe_by_name(self, name):
        self._db_cur.execute("SELECT * FROM recipe WHERE name = :name", {"name": name})
        return self._db_cur.fetchone()

    def get_all_recipes(self):
        self._db_cur.execute("SELECT * FROM recipe")
        return self._db_cur.fetchall()

    # Update
    def update_ingredient(self, id, changes):

        to_change = changes.keys()
        # TODO: make this error better
        if "id" in to_change:
            print("ID cannot be changed")
            return
        if "type" in to_change:
            type_number = changes["type"].value
            changes["type"] = type_number

        self._db_cur.execute("SELECT * FROM ingredient WHERE id = ?", (str(id)))
        values = dict(self._db_cur.fetchone())
        values.update(changes)

        with self._db_conn:
            self._db_cur.execute(
                """
                UPDATE ingredient
                SET name = :name,
                amount_per_unit = :amount_per_unit,
                price_per_unit = :price_per_unit,
                type = :type,
                unit = :unit
                WHERE id = :id
                """,
                values,
            )

    def update_recipe(self, id, changes):
        to_change = changes.keys()
        # TODO: make this error better
        if "id" in to_change:
            print("ID cannot be changed")
            return
        if "ingredients" in to_change:
            with self._db_conn:
                self._db_cur.execute(
                    "DELETE FROM recipe_ingredient WHERE recipe_id = ?", (str(id))
                )
            self.insert_recipe_ingredients(id, changes["ingredients"])
            del changes["ingredients"]

        self._db_cur.execute("SELECT * FROM recipe WHERE id = ?", (str(id)))
        values = dict(self._db_cur.fetchone())
        values.update(changes)

        with self._db_conn:
            self._db_cur.execute(
                """
                UPDATE recipe
                SET name = :name,
                servings = :servings,
                serving_unit = :serving_unit,
                sale_price = :sale_price
                WHERE id = :id
                """,
                values,
            )

    # Delete
    def delete_ingredient(self, id):
        with self._db_conn:
            self._db_cur.execute(
                "DELETE FROM recipe_ingredient WHERE ingredient_id = ?", (str(id))
            )
            self._db_cur.execute("DELETE FROM ingredient WHERE id = ?", (str(id)))

    def delete_recipe(self, id):
        with self._db_conn:
            self._db_cur.execute(
                "DELETE FROM recipe_ingredient WHERE recipe_id = ?", (str(id))
            )
            self._db_cur.execute("DELETE FROM recipe WHERE id = ?", (str(id)))
