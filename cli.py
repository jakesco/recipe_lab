#!/usr/bin/env python

import recipelab.core


class RecipeLabCLI:
    def __init__(self):
        self.rl = recipelab.core.RecipeLab(":memory:")
        with open("tests/sample_data.sql") as f:
            self.rl.db._db_cur.executescript(f.read())

    def list_recipes(self):
        recipes = self.rl.list_recipes()
        print("Recipes:")
        for recipe in recipes:
            print(f"{recipe.name} - {len(recipe.ingredients)}")
        print()

    def list_ingredients(self):
        ingredients = self.rl.list_ingredients()
        print("Ingredients:")
        for ingredient in ingredients:
            print(f"{ingredient.name}")
        print()

    def recipe_detail(recipe):
        pass


if __name__ == "__main__":
    cli = RecipeLabCLI()
    cli.list_recipes()
    cli.list_ingredients()
