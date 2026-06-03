from domain import ingredient
from domain.ingredient import Ingredient
from domain.recipe import Recipe

import pytest

class TestIngredient:
    def test_init(self):
        ingredient = Ingredient("Мука", 500, "г")
        assert ingredient.name == 'Мука'
        assert ingredient.quantity == 500.0
        assert ingredient.unit == 'г'

    def test_negative_quantity(self):
        with pytest.raises(ValueError):
            Ingredient("Мука", -500, 'г')

    def test_zero_quantity(self):
        with pytest.raises(ValueError):
            Ingredient("Мука", 0, 'г')

    def test_str(self):
        ingredient = Ingredient("Мука", 500, "г")
        assert str(ingredient) == "Мука: 500.0 г"

    def test_eq_different_quantity(self):
        ingredient1 = Ingredient("Мука", 500, "г")
        ingredient2 = Ingredient("Мука", 200, "г")
        assert ingredient1 == ingredient2

    def test_eq_different_names(self):
        ingredient1 = Ingredient("Мука", 500, "г")
        ingredient2 = Ingredient("Мясо", 500, "г")
        assert ingredient1 != ingredient2

    def test_eq_different_units(self):
        ingredient1 = Ingredient("Мука", 500, "г")
        ingredient2 = Ingredient("Мука", 500, "кг")
        assert ingredient1 != ingredient2

class TestRecipe:
    def test_init(self):
        ingredients = [Ingredient("Мука", 500, "г"), Ingredient("Курица", 200, "г")]
        recipe = Recipe("Пицца", ingredients)
        assert recipe.title == "Пицца"
        assert recipe.ingredients == ingredients

    def test_add_new_ingredient(self):
        recipe = Recipe("Пицца")
        ingredient = Ingredient("Мука", 500, "г")
        recipe.add_ingredient(ingredient)
        assert len(recipe.ingredients) == 1
        assert recipe.ingredients[0] == ingredient

    def test_existing_ingredient(self):
        recipe = Recipe("Пицца")
        recipe.add_ingredient(Ingredient("Мука", 500, "г"))
        recipe.add_ingredient(Ingredient("Мука", 200, "г"))
        assert len(recipe.ingredients) == 1
        assert recipe.ingredients[0].quantity == 700.0

    def test_scale_new_list(self):
        ingredients = [Ingredient("Мука", 500, "г"), Ingredient("Курица", 200, "г")]
        recipe = Recipe("Пицца", ingredients)
        new_recipe = recipe.scale(2)
        assert recipe != new_recipe

    def test_scale_quantities(self):
        ingredients = [Ingredient("Мука", 500, "г"), Ingredient("Курица", 200, "г")]
        recipe = Recipe("Пицца", ingredients)
        new_recipe = recipe.scale(2)
        for i in range(2):
            assert new_recipe.ingredients[i].quantity == recipe.ingredients[i].quantity * 2

    def test_negative_ratio(self):
        ingredients = [Ingredient("Мука", 500, "г"), Ingredient("Курица", 200, "г")]
        recipe = Recipe("Пицца", ingredients)
        with pytest.raises(ValueError):
            recipe.scale(-2)

    def test_len(self):
        ingredients = [Ingredient("Мука", 500, "г"), Ingredient("Курица", 200, "г")]
        recipe = Recipe("Пицца", ingredients)
        assert len(recipe) == 2

    def test_len_with_dublicates(self):
        recipe = Recipe("Пицца")
        recipe.add_ingredient(Ingredient("Мука", 500, "г"))
        recipe.add_ingredient(Ingredient("Мука", 200, "г"))
        assert len(recipe) == 1