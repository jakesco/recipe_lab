import sqlite3
import os
from .objects import Recipe, Ingredient

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
    def insert_ingredient(self, ingredient):
        with self._db_conn:
            self._db_cur.execute(
                "INSERT INTO ingredient VALUES (?, ?, ?, ?, ?, ?)",
                (
                    ingredient.id,
                    ingredient.name,
                    ingredient.amount_per_unit,
                    ingredient.price_per_unit,
                    ingredient.type.value,
                    ingredient.unit,
                ),
            )

    def insert_recipe_ingredients(self, recipe_id, ingredients):
        with self._db_conn:
            for i in ingredients:
                self._db_cur.execute(
                    "INSERT INTO recipe_ingredient VALUES (?, ?, ?)",
                    (recipe_id, i[0], i[1]),
                )

    def insert_recipe(self, recipe):
        with self._db_conn:
            self._db_cur.execute(
                "INSERT INTO recipe VALUES (?, ?, ?, ?, ?)",
                (
                    recipe.id,
                    recipe.name,
                    recipe.servings,
                    recipe.serving_unit,
                    recipe.sale_price,
                ),
            )

        # Database may assign a different id, this ensures we have the correct id
        self._db_cur.execute(
            "SELECT id FROM recipe WHERE name = :name", {"name": recipe.name}
        )
        recipe_id = self._db_cur.fetchone()[0]

        self.insert_recipe_ingredients(recipe_id, recipe.ingredients)

    # Retrieve
    def get_ingredient(self, id):
        self._db_cur.execute("SELECT * FROM ingredient WHERE id = ?", (str(id)))
        row = self._db_cur.fetchone()
        return Ingredient(
            row["name"],
            row["amount_per_unit"],
            row["price_per_unit"],
            Ingredient.Type(row["type"]),
            row["unit"],
            row["id"],
        )

    def get_all_ingredients(self):
        self._db_cur.execute("SELECT * FROM ingredient")
        return list(
            map(
                lambda row: Ingredient(
                    row["name"],
                    row["amount_per_unit"],
                    row["price_per_unit"],
                    Ingredient.Type(row["type"]),
                    row["unit"],
                    row["id"],
                ),
                self._db_cur.fetchall(),
            )
        )

    def get_ingredients_for_recipe(self, recipe_id):
        self._db_cur.execute(
            "SELECT * FROM recipe_ingredient WHERE recipe_id = ?", (str(recipe_id))
        )
        return list(
            map(lambda x: (x["ingredient_id"], x["amount"]), self._db_cur.fetchall())
        )

    def get_recipe(self, id):
        self._db_cur.execute("SELECT * FROM recipe WHERE id = ?", (str(id)))
        row = self._db_cur.fetchone()
        return Recipe(
            row["name"],
            row["servings"],
            row["serving_unit"],
            row["sale_price"],
            self.get_ingredients_for_recipe(id),
            row["id"],
        )

    def get_all_recipes(self):
        self._db_cur.execute("SELECT * FROM recipe")
        return list(
            map(
                lambda row: Recipe(
                    row["name"],
                    row["servings"],
                    row["serving_unit"],
                    row["sale_price"],
                    self.get_ingredients_for_recipe(row["id"]),
                    row["id"],
                ),
                self._db_cur.fetchall(),
            )
        )

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
