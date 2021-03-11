PRAGMA foreign_keys = ON;

CREATE TABLE ingredient (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    amount_per_unit REAL NOT NULL,
    price_per_unit REAL NOT NULL,
    type INTEGER NOT NULL CHECK(type in (1, 2, 3)),
    unit TEXT
);

CREATE TABLE recipe (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    servings REAL NOT NULL,
    serving_unit TEXT,
    sale_price REAL NOT NULL
);

CREATE TABLE recipe_ingredient (
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    PRIMARY KEY(recipe_id, ingredient_id)
    FOREIGN KEY(recipe_id) REFERENCES recipe(id),
    FOREIGN KEY(ingredient_id) REFERENCES ingredient(id)
);