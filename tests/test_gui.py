import context

from recipelab.gui import MainWindow
from recipelab.api import RecipeLabAPI

if __name__ == "__main__":
    api = RecipeLabAPI()
    with open("./sample_data.sql") as f:
        api.repo._db._db_cur.executescript(f.read())
    api.repo.refresh()

    rlw = MainWindow(api)
    rlw.mainloop()

