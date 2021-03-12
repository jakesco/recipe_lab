import sqlite3
from ingredient import Ingredient
from recipe import Recipe
from pprint import pprint

# conn = sqlite3.connect("recipelab.db")
conn = sqlite3.connect(":memory:")

c = conn.cursor()


def init_db():
    with open("recipelab/schema.sql") as f:
        c.executescript(f.read())


def insert_ingredient(ingredient):
    with conn:
        c.execute(
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


def update_ingredient(id, changes):
    sql = ["UPDATE ingredient SET"]
    for k in changes.keys():
        sql.append(f"{k} = :{k}")
        sql.append(",")
    del sql[-1]
    sql.append("WHERE id = :id")
    changes["id"] = id
    query = " ".join(sql)

    with conn:
        c.execute(query, changes)


def delete_ingredient(id):
    with conn:
        c.execute("DELETE FROM ingredient WHERE id = ?", (str(id)))


def find_ingredient(id):
    with conn:
        c.execute("SELECT * FROM ingredient WHERE id = ?", (str(id)))

    match = c.fetchone()
    return Ingredient(
        match[1], match[2], match[3], Ingredient.Type(match[4]), match[5], match[0]
    )


def insert_recipe(recipe):
    with conn:
        c.execute(
            "INSERT INTO recipe VALUES (?, ?, ?, ?, ?)",
            (
                recipe.id,
                recipe.name,
                recipe.servings,
                recipe.serving_unit,
                recipe.sale_price,
            ),
        )

    c.execute("SELECT id FROM recipe WHERE name = :name", {"name": recipe.name})
    recipe_id = c.fetchone()[0]

    with conn:
        for i in recipe.ingredients:
            c.execute(
                "INSERT INTO recipe_ingredient VALUES (?, ?, ?)",
                (recipe_id, i[0], i[1]),
            )


def get_recipe_by_name(name):
    c.execute("SELECT * FROM recipe WHERE name = :name", {"name": name})
    query = c.fetchone()
    print(query)
    print(get_ingredients_for_recipe(query[0]))


def get_ingredients_for_recipe(recipe_id):
    c.execute("SELECT * FROM recipe_ingredient WHERE recipe_id = ?", (recipe_id))
    return c.fetchall()


def get_all_ingredients():
    c.execute("SELECT * FROM ingredient")
    query = []
    for row in c.fetchall():
        query.append(
            Ingredient(row[1], row[2], row[3], Ingredient.Type(row[4]), row[5], row[0])
        )
    return query


init_db()

ingredients = [
    Ingredient("Unsalted Crackers", 140, 1.23, Ingredient.Type.OTHER, "cracker"),
    Ingredient("Unsalted Butter", 16, 2.94, Ingredient.Type.DRY),
    Ingredient("Brown Sugar", 32, 2.73, Ingredient.Type.DRY),
    Ingredient("Salt", 4.4, 0.98, Ingredient.Type.DRY),
    Ingredient("Vanilla Extract", 2, 4.98, Ingredient.Type.FLUID),
    Ingredient("Semi-Sweet Chocolate Chips", 12, 1.74, Ingredient.Type.DRY),
]

for i in ingredients:
    insert_ingredient(i)

recipe = Recipe(
    "Chocolate Caramel Toffee",
    24,
    "crackers",
    20.00,
    [(1, 40), (2, 8), (3, 8), (4, 0.05), (5, 0.87), (6, 12)],
)

insert_recipe(recipe)

pprint(get_all_ingredients())

update_ingredient(1, {"name": "test name", "amount_per_unit": 20})

print()
pprint(get_all_ingredients())

conn.close()