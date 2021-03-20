import tkinter as tk
from tkinter import ttk
from tkinter import N, S, E, W


# TODO: Install python3-tkinter


class RecipeLabMainWindow:
    def __init__(self, root):
        root.title("Recipe Lab")
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, S, E, W))

        self.search = tk.StringVar()
        search_box = ttk.Entry(mainframe, width=20, textvariable=self.search)
        search_box.grid(column=0, row=0, sticky=(N, W))

        self.list = ttk.Treeview(mainframe)


if __name__ == "__main__":
    root = tk.Tk()
    RecipeLabMainWindow(root)
    root.mainloop()
