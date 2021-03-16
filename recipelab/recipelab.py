from .db import DB
from .recipe import Recipe
from .ingredient import Ingredient


class RecipeLab:
    def __init__(self, db_path):
        self.db = DB(db_path)