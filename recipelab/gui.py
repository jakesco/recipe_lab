import tkinter as tk
from tkinter import ttk
from tkinter import N, S, E, W

from ingredient import Ingredient
import core


class RecipeLabMainWindow:
    def __init__(self, root, ingredients):
        root.title("Recipe Lab")
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, S, E, W))

        self.search = tk.StringVar()
        search_box = ttk.Entry(mainframe, width=20, textvariable=self.search)
        search_box.grid(column=0, row=0, sticky=(N, W))
        self.search.trace_add("write", self.narrow_list)

        self.tree = ttk.Treeview(mainframe, columns=("cost"))
        self.tree.grid(column=0, row=1, sticky=(N, W))
        self.tree.heading("cost", text="Cost")
        self.tree.column("cost", width=100)

        search_box.focus()

        self.set_ingredients(ingredients)

    def set_ingredients(self, ingredients):
        self.ingredients = ingredients
        for i in self.ingredients:
            self.tree.insert(
                "",
                "end",
                i.name,
                text=i.name,
                values=(f"${i.cost_per_unit:.2f}"),
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
        Ingredient("Test Ing 1", 100, 100, Ingredient.Type),
        Ingredient("Test Ing 2", 100, 25, Ingredient.Type.FLUID),
        Ingredient("Test Ing 3", 100, 50, Ingredient.Type.OTHER, "tests"),
        Ingredient("Another one", 100, 100, Ingredient.Type),
        Ingredient("Sausage", 100, 25, Ingredient.Type.FLUID),
        Ingredient("Sauce", 100, 50, Ingredient.Type.OTHER, "tests"),
    ]

    root = tk.Tk()
    rlw = RecipeLabMainWindow(root, i)
    root.mainloop()
