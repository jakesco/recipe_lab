import unittest
from recipelab.ingredient import Ingredient


class TestIngredient(unittest.TestCase):
    def test_ingredient(self):
        x = Ingredient(1, "name", 2, "cups", 20)
        print(x)
        print(x.to_dict())


if __name__ == "__main__":
    unittest.main()
