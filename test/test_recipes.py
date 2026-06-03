from domain import ingredient
from domain.ShoppingList import ShoppingList
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

    def test_len_with_duplicate(self):
        recipe = Recipe("Пицца")
        recipe.add_ingredient(Ingredient("Мука", 500, "г"))
        recipe.add_ingredient(Ingredient("Мука", 200, "г"))
        assert len(recipe) == 1

class TestShoppingList:
    def test_add_recipe(self):
        ingredients = [Ingredient("Мука", 500, "г"), Ingredient("Курица", 200, "г")]
        recipe = Recipe("Пицца", ingredients)
        shopping_list = ShoppingList()
        shopping_list.add_recipe(recipe, 2)
        res = shopping_list.get_list()
        assert len(res) == 2
        assert res[0].name == "Курица"
        assert res[0].quantity == 400.0
        assert res[1].name == "Мука"
        assert res[1].quantity == 1000.0

    def test_add_recipe_negative_portions(self):
        recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
        shopping_list = ShoppingList()
        with pytest.raises(ValueError):
            shopping_list.add_recipe(recipe, -1)

    def test_add_recipe_zero_portions(self):
        recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
        shopping_list = ShoppingList()
        with pytest.raises(ValueError):
            shopping_list.add_recipe(recipe, 0)

    def test_remove_recipe(self):
        recipe1 = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
        recipe2 = Recipe("Стейк", [Ingredient("Курица", 200, "г")])
        shopping_list = ShoppingList()
        shopping_list.add_recipe(recipe1, 1)
        shopping_list.add_recipe(recipe2, 1)
        shopping_list.remove_recipe("Пицца")
        result = shopping_list.get_list()
        assert len(result) == 1
        assert result[0].name == "Курица"

    def test_remove_missing_recipe(self):
        recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
        shopping_list = ShoppingList()
        shopping_list.add_recipe(recipe, 1)
        shopping_list.remove_recipe("Стейк")
        result = shopping_list.get_list()
        assert len(result) == 1
        assert result[0].name == "Мука"

    def test_get_list_sums_ingredients(self):
        recipe1 = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
        recipe2 = Recipe("Пирог", [Ingredient("Мука", 300, "г")])
        shopping_list = ShoppingList()
        shopping_list.add_recipe(recipe1, 1)
        shopping_list.add_recipe(recipe2, 1)
        result = shopping_list.get_list()
        assert len(result) == 1
        assert result[0].name == "Мука"
        assert result[0].quantity == 800.0

    def test_get_list_sorted(self):
        ingredients = [
            Ingredient("Курица", 200, "г"),
            Ingredient("Мука", 500, "г"),
            Ingredient("Кетчуп", 200, "мл")
        ]
        recipe = Recipe("Пицца", ingredients)
        shopping_list = ShoppingList()
        shopping_list.add_recipe(recipe, 1)
        result = shopping_list.get_list()
        assert result[0].name == "Кетчуп"
        assert result[1].name == "Курица"
        assert result[2].name == "Мука"

    def test_add_shopping_lists_not_change_old_lists(self):
        recipe1 = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
        recipe2 = Recipe("Стейк", [Ingredient("Курица", 200, "г")])
        shopping_list1 = ShoppingList()
        shopping_list2 = ShoppingList()
        shopping_list1.add_recipe(recipe1, 1)
        shopping_list2.add_recipe(recipe2, 1)
        new_shopping_list = shopping_list1 + shopping_list2
        assert len(shopping_list1.get_list()) == 1
        assert len(shopping_list2.get_list()) == 1
        assert len(new_shopping_list.get_list()) == 2

    def test_add_shopping_lists(self):
        recipe1 = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
        recipe2 = Recipe("Стейк", [Ingredient("Курица", 200, "г")])
        shopping_list1 = ShoppingList()
        shopping_list2 = ShoppingList()
        shopping_list1.add_recipe(recipe1, 1)
        shopping_list2.add_recipe(recipe2, 1)
        new_shopping_list = shopping_list1 + shopping_list2
        result = new_shopping_list.get_list()
        assert len(result) == 2
        assert result[0].name == "Курица"
        assert result[1].name == "Мука"