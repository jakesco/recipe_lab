import json
import tkinter as tk

from tkinter import ttk
from tkinter import N, S, E, W

UNITS = ('tsp', 'tbsp', 'cup', 'oz', 'floz')


class MainWindow(tk.Tk):
    def __init__(self, api):
        tk.Tk.__init__(self)

        self.title("Recipe Lab")
        self.style = ttk.Style()
        self.style.configure('Treeview', rowheight=25)

        notebook = ttk.Notebook(self)
        notebook.pack(padx=5, pady=5, expand=True)

        recipe_frame = RecipeListFrame(notebook, api)
        ingredient_frame = IngredientListFrame(notebook, api)

        notebook.add(ingredient_frame, text="Ingredient List")
        notebook.add(recipe_frame, text="Recipes")


class IngredientListFrame(ttk.Frame):
    def __init__(self, parent, api):
        ttk.Frame.__init__(self, parent)
        self.api = api
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
        self.tree.grid(column=0, row=1, columnspan=2, sticky=(N, W, E))
        self.tree.heading("#0", text="Name")  # Set first column name
        self.tree.heading("package", text="Amount in Package")
        self.tree.heading("package_cost", text="Cost")
        self.tree.heading("cost_unit", text="Cost per Unit")
        self.tree.column("#0", width=300)
        self.tree.column("package", width=200)
        self.tree.column("package_cost", width=100)
        self.tree.column("cost_unit", width=200)

        self.item_ids = tuple()
        self.refresh()

        search_box.focus()

    def refresh(self):
        """Sets initial ingredients in list"""
        self.tree.delete(*self.item_ids)
        message = json.loads(self.api.all_ingredients())
        ingredients = message["content"]
        for i in ingredients:
            self.tree.insert(
                "",
                "end",
                i["id"],
                text=i["name"],
                values=(
                    f"{i['amount']:.1f} {i['unit']}(s)",
                    f"${i['cost']:.2f}",
                    f"${i['cost']/i['amount']:.2f} per {i['unit']}",
                ),
            )
        self.item_ids = self.tree.get_children()

    def fuzzy_name_search(self, *args):
        """Narrows recipe list from search box"""
        search_term = self.search.get().lower()
        # 'names' is a list of (id, name) in tree
        names = [(i, self.tree.item(i)['text']) for i in self.item_ids]
        result = [n for _, n in names if search_term in n.lower()]
        for i, n in names:
            if n in result:
                # This will put detached names back in the list
                self.tree.move(i, "", "end")
            else:
                self.tree.detach(i)

    def spawn_new_ingredient_window(self):
        NewIngredientWindow(self, self.api)


class NewIngredientWindow(tk.Toplevel):
    def __init__(self, parent, api):
        tk.Toplevel.__init__(self, parent)
        self.title("Recipe Lab - New Ingredient")
        self.parent = parent
        self.api = api

        s = ttk.Style()
        s.configure('Success.TLabel', foreground='green')
        s.configure('Failed.TLabel', foreground='red')

        # Name Entry
        self.name = tk.StringVar()
        name_box_label = ttk.Label(self, text="Name:")
        name_box_label.grid(column=0, row=0, sticky=(N, W))
        name_box = ttk.Entry(self, width=20, textvariable=self.name)
        name_box.grid(column=1, row=0, sticky=(N, W))

        # Amount in package Entry
        self.package_amount = tk.StringVar()
        ttk.Label(self, text="Amount in package:").grid(column=0, row=2, sticky=(N, W))
        package_amount_box = ttk.Entry(self, width=20, textvariable=self.package_amount)
        package_amount_box.grid(column=1, row=2, sticky=(N, W))

        # Type Combobox
        self.unit = tk.StringVar()
        unit_box = ttk.Combobox(self, textvariable=self.unit)
        unit_box.grid(column=2, row=2, sticky=W)
        unit_box['values'] = UNITS

        # Cost per package
        self.package_cost = tk.StringVar()
        ttk.Label(self, text="Cost of package:").grid(column=0, row=3, sticky=(N, W))
        package_cost_box = ttk.Entry(self, width=20, textvariable=self.package_cost)
        package_cost_box.grid(column=1, row=3, sticky=(N, W))

        # Feedback
        self.feedback = tk.StringVar()
        self.feedback_label = ttk.Label(self, textvariable=self.feedback)
        self.feedback_label.grid(column=0, row=4, columnspan=3, sticky=(S, W))

        # Submit
        self.submit_btn = ttk.Button(self, text="Add", command=self.create_ingredient)
        self.submit_btn.grid(column=3, row=4, sticky=E)

        name_box.focus()

    def create_ingredient(self):
        self.submit_btn['state'] = 'disabled'
        message = {"name": self.name.get(),
                   "amount": float(self.package_amount.get()),
                   "unit": self.unit.get(),
                   "cost": float(self.package_cost.get())}
        result = json.loads(self.api.new_ingredient(json.dumps(message)))

        self.feedback_label['style'] = 'Success.TLabel' if result["status"] else 'Failed.TLabel'
        self.feedback.set(result['content'])

        self.submit_btn['state'] = 'normal'
        self.parent.refresh()


class RecipeListFrame(ttk.Frame):
    def __init__(self, parent, repository):
        ttk.Frame.__init__(self, parent)
        self.grid(column=0, row=0, sticky=(N, S, E, W))
        self.api = repository
        self.parent = parent

        self.grid(column=0, row=0, sticky=(N, S, E, W))

        self.search = tk.StringVar()
        search_box = ttk.Entry(self, width=20, textvariable=self.search)
        search_box.grid(column=0, row=0, sticky=(N, W, E))
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
        self.tree.column("#0", width=300)
        self.tree.column("servings", width=100)
        self.tree.column("cost", width=100)
        self.tree.column("sale_price", width=100)
        self.tree.column("profit", width=100)

        self.item_ids = tuple()
        self.refresh()

        search_box.focus()

    def refresh(self):
        """Sets initial ingredients in list"""
        self.tree.delete(*self.item_ids)
        message = json.loads(self.api.all_recipes())
        recipes = message["content"]
        for r in recipes:
            self.tree.insert(
                "",
                "end",
                r["id"],
                text=r["name"],
                values=(
                    "{:.1f} {}".format(r['servings'], "" if r["serving_unit"] is None else r["serving_unit"]),
                    f"${r['cost']:.2f}",
                    f"${r['sale_price']:.2f}",
                    f"${r['profit']:.2f}"
                ),
            )
        self.item_ids = self.tree.get_children()

    def fuzzy_name_search(self, *args):
        """Narrows recipe list from search box"""
        search_term = self.search.get().lower()
        # 'names' is a list of (id, name) in tree
        names = [(i, self.tree.item(i)['text']) for i in self.item_ids]
        result = [n for _, n in names if search_term in n.lower()]
        for i, n in names:
            if n in result:
                # This will put detached names back in the list
                self.tree.move(i, "", "end")
            else:
                self.tree.detach(i)

    def spawn_new_recipe_window(self):
        NewRecipeWindow(self, self.api)


class NewRecipeWindow(tk.Toplevel):
    def __init__(self, parent, api):
        tk.Toplevel.__init__(self, parent)
        self.title("Recipe Lab - New Recipe")
        self.parent = parent
        self.api = api

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
        self.submit_btn = ttk.Button(self, text="Add", command=self.create_recipe)
        self.submit_btn.grid(column=3, row=4, sticky=E)

        name_box.focus()

    def create_recipe(self):
        self.submit_btn['state'] = 'disabled'
        self.api.add_ingredient(
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
