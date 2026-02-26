
from datetime import datetime, timedelta

class Garment:

    def __init__(self, item_id, category, color, season, brand, price, last_worn=None):
        self.item_id = item_id
        self.category = category
        self.color = color
        self.season = season
        self.brand = brand
        self._price = price
        self.last_worn = last_worn

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    def __repr__(self):
        return (
            f"Garment(id={self.item_id}, "
            f"category={self.category}, "
            f"color={self.color}, "
            f"season={self.season}, "
            f"brand={self.brand}, "
            f"price=₪{self.price})"
        )
