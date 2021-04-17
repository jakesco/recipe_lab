import json

from . import log
from .repository import Repository


def success(content=None, **kw) -> str:
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
        args = json.loads(message)
        if args.keys() < {"name", "servings", "sale_price"}:
            message = "Required keys not present (name, servings, sale_price)."
            log.error(message)
            return failed(message)
        try:
            self.repo.new_recipe(args["name"],
                                 args["servings"],
                                 args["sale_price"],
                                 args.get("serving_unit"),
                                 args.get("ingredients_list"))
            return success()
        except Exception as e:
            message = f"Failed to create new recipe ({e})."
            log.error(message)
            return failed(message)

    def get_ingredients(self, message: str) -> str:
        args = json.loads(message)
        if args.keys() < {"ids"}:
            message = "Required keys not present (ids)."
            log.error(message)
            return failed(message)
        try:
            ids = args["ids"]
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

    def get_recipes(self, message: str) -> str:
        args = json.loads(message)
        if args.keys() < {"ids"}:
            message = "Required keys not present (ids)."
            log.error(message)
            return failed(message)
        try:
            ids = args["ids"]
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
        # TODO
        pass

    def update_recipe(self, message: str) -> str:
        # TODO
        pass

    def del_ingredient(self, message: str) -> str:
        args = json.loads(message)
        if args.keys() < {"ingredient_id"}:
            message = "Required keys not present (ingredient_id)."
            log.error(message)
            return failed(message)
        try:
            self.repo.delete_ingredient(args["ingredient_id"])
            return success("Ingredient deleted.")
        except Exception as e:
            message = f"Failed to delete ingredient ({e})."
            log.error(message)
            return failed(message)

    def del_recipe(self, message: str) -> str:
        args = json.loads(message)
        if args.keys() < {"recipe_id"}:
            message = "Required keys not present (recipe_id)."
            log.error(message)
            return failed(message)
        try:
            self.repo.delete_recipe(args["recipe_id"])
            return success("Recipe deleted.")
        except Exception as e:
            message = f"Failed to delete recipe ({e})."
            log.error(message)
            return failed(message)
