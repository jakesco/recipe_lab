import unittest
from context import DB


class TestCore(unittest.TestCase):
    def setUp(self):
        self.db = DB(":memory:")
        self.db.init_db()

    def test_test(self):
        print("testing")


if __name__ == "__main__":
    unittest.main()
