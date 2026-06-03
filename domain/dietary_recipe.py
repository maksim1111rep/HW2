from domain.recipe import Recipe


class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients: list = None):
        super().__init__(title, ingredients)
        self._diet_type = diet_type

    @property
    def diet_type(self):
        return self._diet_type

    def scale(self, ratio: float):
        new_recipe = super().scale(ratio)
        return DietaryRecipe(new_recipe.title, self._diet_type, new_recipe.ingredients)

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"