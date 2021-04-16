import context

from recipelab.gui import MainWindow
from recipelab.repository import Repository

if __name__ == "__main__":
    repo = Repository()
    repo._db.init_db()
    with open("./sample_data.sql") as f:
        repo._db._db_cur.executescript(f.read())
    repo.refresh()

    rlw = MainWindow(repo)
    rlw.mainloop()

