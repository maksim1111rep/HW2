from packaging.pylock import is_valid_pylock_path

from domain import ingredient
from domain.ingredient import Ingredient


class Recipe:
    def __init__(self, title: str, ingredients: list[Ingredient] = None):
        self._title = title
        if ingredients:
            self._ingredients = ingredients
        else:
            self._ingredients = []

    @property
    def title(self):
        return self._title

    @property
    def ingredients(self):
        return self._ingredients

    def add_ingredient(self, ingredient: Ingredient):
        ind = -1
        if ingredient in self._ingredients:
            ind = self._ingredients.index(ingredient)
        if ind != -1:
            self._ingredients[ind].quantity += ingredient.quantity
        else:
            self._ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(val) -> bool:
        if isinstance(val, int) or isinstance(val, float):
            return val > 0
        return False

    def scale(self, ratio: float):
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Передан коэффицент меньше 0")
        out = []
        for ingredient in self._ingredients:
            out.append(Ingredient(ingredient.name, ingredient.quantity * ratio, ingredient.unit))
        return Recipe(self.title, out)

    def __len__(self):
        return len(self._ingredients)

    def __str__(self):
        out = f'Название блюда: {self._title}\n'
        out += "Рецепт:"
        for ingredient in self._ingredients:
            out += f'{ingredient.name}\n'
        return out