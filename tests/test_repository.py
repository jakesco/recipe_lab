import unittest
from recipelab.repository import Repository, Ingredient, Recipe


class TestRepository(unittest.TestCase):

    def setUp(self):
        self.repo = Repository()

        with open("./sample_data.sql") as f:
            self.repo._db._db_cur.executescript(f.read())

        self.repo.refresh()

    def test_init_repo(self):
        print(self.repo)


if __name__ == "__main__":
    unittest.main()
