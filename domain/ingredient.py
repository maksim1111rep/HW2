class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self._name = name
        self.quantity = quantity
        self._unit = unit

    @property
    def name(self):
        return self._name

    @property
    def unit(self):
        return self._unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, val):
        if val <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(val)

    def __str__(self):
        return f'{self._name}: {self._quantity} {self.unit}'

    def __repr__(self):
        return f"Ingredient('{self._name}', {self._quantity}, '{self._unit}')"

    def __eq__(self, other):
        return self._name == other._name and self._unit == other._unit
