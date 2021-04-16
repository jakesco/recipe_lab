import json

from . import log
from .repository import Repository


def success(content = None, **kw) -> str:
    if content is None:
        return json.dumps({"status": True}, **kw)
    message = {"status": True, "content": content}
    return json.dumps(message, **kw)


def failed(content: str, **kw) -> str:
    message = {"status": False, "content": content}
    return json.dumps(message, **kw)


class RecipeLabAPI:
    def __init__(self, db_path=":memory:"):
        self.repo = Repository(db_path)
        log.info("Initialized API.")

    def new_ingredient(self, message: str) -> str:
        args = json.loads(message)
        if args.keys() < {"name", "amount", "unit", "cost"}:
            message = "Keys not present (name, amount, unit, cost)."
            log.error(message)
            return failed(message)
        try:
            self.repo.new_ingredient(args["name"], args["amount"], args["unit"], args["cost"])
            return success()
        except Exception as e:
            message = f"Failed to create new ingredient ({e})."
            log.error(message)
            return failed(message)

    def new_recipe(self, message: str) -> str:
        pass

    def get_ingredients(self, ids: tuple[int, ...]) -> str:
        try:
            message = [self.repo.get_ingredient(i).to_dict() for i in ids]
            return success(message, indent=2)
        except Exception as e:
            message = f"Failed to fetch ingredients ({e})."
            log.error(message)
            return failed(message)

    def all_ingredients(self) -> str:
        try:
            ingredients = self.repo.list_ingredients()
            message = [i.to_dict() for i in ingredients]
            return success(message, indent=2)
        except Exception as e:
            message = f"Failed to fetch ingredients ({e})."
            log.error(message)
            return failed(message)

    def get_recipes(self, ids: tuple[int, ...]) -> str:
        try:
            message = [self.repo.get_recipe(i).to_dict() for i in ids]
            return success(message, indent=2)
        except Exception as e:
            message = f"Failed to fetch recipes ({e})."
            log.error(message)
            return failed(message)

    def all_recipes(self) -> str:
        try:
            recipes = self.repo.list_recipes()
            message = [r.to_dict() for r in recipes]
            return success(message, indent=2)
        except Exception as e:
            message = f"Failed to fetch recipes ({e})."
            log.error(message)
            return failed(message)

    def update_ingredient(self, message: str) -> str:
        pass

    def update_recipe(self, message: str) -> str:
        pass

    def del_ingredient(self, message: str) -> str:
        pass

    def del_recipe(self, message: str) -> str:
        pass