import tkinter as tk
from tkinter import ttk
from tkinter import N, S, E, W

from ingredient import Ingredient
import core


class RecipeLabMainWindow:
    def __init__(self, root, ingredients):
        root.title("Recipe Lab")

        notebook = ttk.Notebook(root)
        notebook.pack(padx=5, pady=5, expand=True)

        ingredient_frame = ttk.Frame(notebook, width=350, height=250)
        recipe_frame = ttk.Frame(notebook, width=350, height=250)

        ingredient_frame.grid(column=0, row=0, sticky=(N, S, E, W))

        self.search = tk.StringVar()
        search_box = ttk.Entry(ingredient_frame, width=20, textvariable=self.search)
        search_box.grid(column=0, row=0, sticky=(N, W))
        self.search.trace_add("write", self.narrow_list)

        self.tree = ttk.Treeview(
            ingredient_frame, columns=("package", "package_cost", "cost_unit")
        )
        self.tree.grid(column=0, row=1, sticky=(N, W))
        self.tree.heading("package", text="Amount in Package")
        self.tree.heading("package_cost", text="Package Cost")
        self.tree.heading("cost_unit", text="Cost per Unit")
        self.tree.column("package", width=200)
        self.tree.column("package_cost", width=200)
        self.tree.column("cost_unit", width=200)

        search_box.focus()

        self.set_ingredients(ingredients)

        notebook.add(ingredient_frame, text="Ingredients")
        notebook.add(recipe_frame, text="Recipes")

    def set_ingredients(self, ingredients):
        self.ingredients = ingredients
        for i in self.ingredients:
            self.tree.insert(
                "",
                "end",
                i.name,
                text=i.name,
                values=(
                    f"{i.package_amount:.0f} {i.unit}(s)",
                    f"${i.package_cost:.2f}",
                    f"${i.cost_per_unit:.2f} per {i.unit}",
                ),
            )

    def refresh_ingredients_list(self, new_ingredients):
        names = list(map(lambda i: i.name, new_ingredients))
        for i in self.ingredients:
            if i.name in names:
                self.tree.move(i.name, "", "end")
            else:
                self.tree.detach(i.name)

    def narrow_list(self, *args):
        result = core.fuzzy_name_search(self.search.get(), self.ingredients)
        self.refresh_ingredients_list(result)


if __name__ == "__main__":
    i = [
        Ingredient("Test Ing 1", 100, 100, Ingredient.Type.DRY),
        Ingredient("Test Ing 2", 100, 25, Ingredient.Type.FLUID),
        Ingredient("Test Ing 3", 100, 50, Ingredient.Type.OTHER, "tests"),
        Ingredient("Another one", 100, 100, Ingredient.Type.DRY),
        Ingredient("Sausage", 100, 25, Ingredient.Type.FLUID),
        Ingredient("Sauce", 100, 50, Ingredient.Type.OTHER, "tests"),
    ]

    root = tk.Tk()
    rlw = RecipeLabMainWindow(root, i)
    root.mainloop()
