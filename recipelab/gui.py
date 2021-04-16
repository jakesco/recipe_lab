import tkinter as tk
from tkinter import ttk
from tkinter import N, S, E, W


class MainWindow(tk.Tk):
    def __init__(self, repository):
        tk.Tk.__init__(self)

        self.title("Recipe Lab")
        self.style = ttk.Style()
        self.style.configure('Treeview', rowheight=25)

        notebook = ttk.Notebook(self)
        notebook.pack(padx=5, pady=5, expand=True)

        recipe_frame = RecipeListFrame(notebook, repository)
        ingredient_frame = IngredientListFrame(notebook, repository)

        notebook.add(recipe_frame, text="Recipes")
        notebook.add(ingredient_frame, text="Ingredient List")


class IngredientListFrame(ttk.Frame):
    def __init__(self, parent, repository):
        ttk.Frame.__init__(self, parent)
        self.repo = repository
        self.parent = parent

        self.grid(column=0, row=0, sticky=(N, S, E, W))

        self.search = tk.StringVar()
        search_box = ttk.Entry(self, width=20, textvariable=self.search)
        search_box.grid(column=0, row=0, sticky=(N, W))
        self.search.trace_add("write", self.fuzzy_name_search)

        new_ingredient_btn = ttk.Button(self, text="New Ingredient", command=self.spawn_new_ingredient_window)
        new_ingredient_btn.grid(column=1, row=0, sticky=E)

        self.tree = ttk.Treeview(
            self, columns=("package", "package_cost", "cost_unit")
        )
        self.tree.grid(column=0, row=1, columnspan=2, sticky=(N, W))
        self.tree.heading("#0", text="Name")  # Set first column name
        self.tree.heading("package", text="Amount in Package")
        self.tree.heading("package_cost", text="Package Cost")
        self.tree.heading("cost_unit", text="Cost per Unit")
        self.tree.column("package", width=200)
        self.tree.column("package_cost", width=200)
        self.tree.column("cost_unit", width=200)

        self.refresh()

        search_box.focus()

    def refresh(self):
        """Sets initial ingredients in list"""
        self.tree.delete(*self.tree.get_children())
        for i in self.repo.all_ingredients():
            self.tree.insert(
                "",
                "end",
                i.__name,
                text=i.__name,
                values=(
                    f"{i.package_amount:.1f} {i.unit}(s)",
                    f"${i.package_cost:.2f}",
                    f"${i.cost_per_unit:.2f} per {i.unit}",
                ),
            )

    def fuzzy_name_search(self, *args):
        """Narrows recipe list from search box"""
        search_term = self.search.get().lower()
        ingredients = self.repo.all_ingredients()
        result = [i.__name for i in ingredients if search_term in i.__name.lower()]
        for i in ingredients:
            if i.__name in result:
                # This will put detached names back in the list
                self.tree.move(i.__name, "", "end")
            else:
                self.tree.detach(i.__name)

    def spawn_new_ingredient_window(self):
        NewIngredientWindow(self, self.repo)


class NewIngredientWindow(tk.Toplevel):
    def __init__(self, parent, repository):
        tk.Toplevel.__init__(self, parent)
        self.title("Recipe Lab - New Ingredient")
        self.parent = parent
        self.repo = repository

        # Name Entry
        self.name = tk.StringVar()
        name_box_label = ttk.Label(self, text="Name:")
        name_box_label.grid(column=0, row=0, sticky=(N, W))
        name_box = ttk.Entry(self, width=20, textvariable=self.name)
        name_box.grid(column=1, row=0, sticky=(N, W))

        # Type Combobox
        self.type = tk.StringVar()
        ttk.Label(self, text="Type:").grid(column=0, row=1, sticky=(N, W))
        ttk.Radiobutton(self, text='DRY', variable=self.type, value=1, command=self.disable_unit_entry).grid(column=1, row=1, sticky=W)
        ttk.Radiobutton(self, text='FLUID', variable=self.type, value=2, command=self.disable_unit_entry).grid(column=1, row=1, sticky=E)
        ttk.Radiobutton(self, text='OTHER', variable=self.type, value=3, command=self.enable_unit_entry).grid(column=2, row=1, sticky=E)

        # Measurement unit Entry
        self.unit = tk.StringVar()
        self.unit_entry = ttk.Entry(self, width=10, textvariable=self.unit)
        self.unit_entry.grid(column=3, row=1, sticky=W)

        self.type.set(1)
        self.disable_unit_entry()

        # Amount in package Entry
        self.package_amount = tk.StringVar()
        ttk.Label(self, text="Amount in package:").grid(column=0, row=2, sticky=(N, W))
        package_amount_box = ttk.Entry(self, width=20, textvariable=self.package_amount)
        package_amount_box.grid(column=1, row=2, sticky=(N, W))

        # Cost per package
        self.package_cost = tk.StringVar()
        ttk.Label(self, text="Cost of package:").grid(column=0, row=3, sticky=(N, W))
        package_cost_box = ttk.Entry(self, width=20, textvariable=self.package_cost)
        package_cost_box.grid(column=1, row=3, sticky=(N, W))

        # Submit
        self.submit_btn = ttk.Button(self, text="Add", command=self.create_ingredient)
        self.submit_btn.grid(column=3, row=4, sticky=E)

        name_box.focus()

    def create_ingredient(self):
        self.submit_btn['state'] = 'disabled'
        self.repo.add_ingredient(
            self.name.get(),
            self.package_amount.get(),
            self.package_cost.get(),
            int(self.type.get()),
            self.unit.get() if self.type.get() == "3" else None
        )
        self.submit_btn['state'] = 'normal'
        self.parent.refresh()

    def enable_unit_entry(self):
        self.unit_entry['state'] = 'normal'
        self.unit_entry.focus()

    def disable_unit_entry(self):
        self.unit_entry['state'] = 'disabled'


class RecipeListFrame(ttk.Frame):
    def __init__(self, parent, repository):
        ttk.Frame.__init__(self, parent)
        self.grid(column=0, row=0, sticky=(N, S, E, W))
        self.repo = repository
        self.parent = parent

        self.grid(column=0, row=0, sticky=(N, S, E, W))

        self.search = tk.StringVar()
        search_box = ttk.Entry(self, width=20, textvariable=self.search)
        search_box.grid(column=0, row=0, sticky=(N, W))
        self.search.trace_add("write", self.fuzzy_name_search)

        new_ingredient_btn = ttk.Button(self, text="New Recipe", command=self.spawn_new_recipe_window)
        new_ingredient_btn.grid(column=1, row=0, sticky=E)

        self.tree = ttk.Treeview(
            self, columns=("servings", "cost", "sale_price", "profit")
        )
        self.tree.grid(column=0, row=1, columnspan=2, sticky=(N, W))
        self.tree.heading("#0", text="Name")  # Set first column name
        self.tree.heading("servings", text="Servings")
        self.tree.heading("cost", text="Cost")
        self.tree.heading("sale_price", text="Sale Price")
        self.tree.heading("profit", text="Profit")
        self.tree.column("servings", width=200)
        self.tree.column("cost", width=200)
        self.tree.column("sale_price", width=200)
        self.tree.column("profit", width=200)

        self.refresh()

        search_box.focus()

    def refresh(self):
        """Sets initial ingredients in list"""
        for r in self.repo.all_recipes():
            self.tree.insert(
                "",
                "end",
                r.__name,
                text=r.__name,
                values=(
                    f"{r.servings:.0f} {r.serving_unit}(s)",
                    f"${r.cost():.2f} ({r.cost_per_serving():.2f} per {r.serving_unit})",
                    f"${r.sale_price:.2f}",
                    f"${r.profit():.2f}",
                ),
            )

    def fuzzy_name_search(self, *args):
        """Narrows recipe list from search box"""
        search_term = self.search.get().lower()
        recipes = self.repo.all_recipes()
        result = [r.__name for r in recipes if search_term in r.__name.lower()]
        for r in recipes:
            if r.__name in result:
                # This will put detached names back in the list
                self.tree.move(r.__name, "", "end")
            else:
                self.tree.detach(r.__name)

    def spawn_new_recipe_window(self):
        NewRecipeWindow(self, self.repo)


class NewRecipeWindow(tk.Toplevel):
    def __init__(self, parent, repository):
        tk.Toplevel.__init__(self, parent)
        self.title("Recipe Lab - New Recipe")
        self.parent = parent
        self.repo = repository

        # Name Entry
        self.name = tk.StringVar()
        name_box_label = ttk.Label(self, text="Name:")
        name_box_label.grid(column=0, row=0, sticky=(N, W))
        name_box = ttk.Entry(self, width=20, textvariable=self.name)
        name_box.grid(column=1, row=0, sticky=(N, W))

        # Type Combobox
        self.type = tk.StringVar()
        ttk.Label(self, text="Type:").grid(column=0, row=1, sticky=(N, W))
        ttk.Radiobutton(self, text='DRY', variable=self.type, value=1, command=self.disable_unit_entry).grid(column=1, row=1, sticky=W)
        ttk.Radiobutton(self, text='FLUID', variable=self.type, value=2, command=self.disable_unit_entry).grid(column=1, row=1, sticky=E)
        ttk.Radiobutton(self, text='OTHER', variable=self.type, value=3, command=self.enable_unit_entry).grid(column=2, row=1, sticky=E)

        # Measurement unit Entry
        self.unit = tk.StringVar()
        self.unit_entry = ttk.Entry(self, width=10, textvariable=self.unit)
        self.unit_entry.grid(column=3, row=1, sticky=W)

        self.type.set(1)
        self.disable_unit_entry()

        # Amount in package Entry
        self.package_amount = tk.StringVar()
        ttk.Label(self, text="Amount in package:").grid(column=0, row=2, sticky=(N, W))
        package_amount_box = ttk.Entry(self, width=20, textvariable=self.package_amount)
        package_amount_box.grid(column=1, row=2, sticky=(N, W))

        # Cost per package
        self.package_cost = tk.StringVar()
        ttk.Label(self, text="Cost of package:").grid(column=0, row=3, sticky=(N, W))
        package_cost_box = ttk.Entry(self, width=20, textvariable=self.package_cost)
        package_cost_box.grid(column=1, row=3, sticky=(N, W))

        # Submit
        self.submit_btn = ttk.Button(self, text="Add", command=self.create_ingredient)
        self.submit_btn.grid(column=3, row=4, sticky=E)

        name_box.focus()

    def create_recipe(self):
        self.submit_btn['state'] = 'disabled'
        self.repo.add_ingredient(
            self.name.get(),
            self.package_amount.get(),
            self.package_cost.get(),
            int(self.type.get()),
            self.unit.get() if self.type.get() == "3" else None
        )
        self.submit_btn['state'] = 'normal'
        self.parent.refresh()