from domain import ingredient
from domain.ingredient import Ingredient

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
