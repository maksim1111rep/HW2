from domain.ingredient import Ingredient
from domain.recipe import Recipe


class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        new_recipe = recipe.scale(portions)
        for ingredient in new_recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title: str):
        new_items = []
        for recipe in self._items:
            if recipe[1] != title:
                new_items.append(recipe)
        self._items = new_items

    def get_list(self):
        data = dict()
        for item in self._items:
            ingredient = item[0]
            if (ingredient.name, ingredient.unit) in data:
                data[(ingredient.name, ingredient.unit)] += ingredient.quantity
            else:
                data[(ingredient.name, ingredient.unit)] = ingredient.quantity
        out = []
        for (name, unit) in data.keys():
            out.append(Ingredient(name, data[(name, unit)], unit))
        out.sort(key=lambda x: x.name)
        return out

    def __add__(self, other):
        new_sl = ShoppingList()
        for item in self._items:
            new_sl._items.append(item)
        for item in other._items:
            new_sl._items.append(item)
        return new_sl