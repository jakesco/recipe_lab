import unittest
from context import Ingredient
from context import RecipeLab


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Testing RecipeLab")

    def setUp(self):
        self.rl = RecipeLab(":memory:")

    def test_new_ingredient(self):
        ret = self.rl.new_ingredient(
            "Unsalted Crackers", 140, 1.23, Ingredient.Type.OTHER, "cracker"
        )
        print(ret)


if __name__ == "__main__":
    unittest.main()
