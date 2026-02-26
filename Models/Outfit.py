from Models.Garment import Garment
class Outfit:

    def __init__(self, outfit_id, season, occasion):
        self.outfit_id = outfit_id
        self.season = season
        self.occasion = occasion
        # Internal list for Garment objects
        self.items = [] 

    # Adds a Garment to the full outfit
    def add_item_to_outfit(self, garment):
        if not isinstance(garment, Garment):
            raise TypeError("Only Garment objects can be added to an Outfit")
        self.items.append(garment)
        return (f"Item '{garment.category}' added successfully.")
    
    # Operator Overloading for readable object representation
    def __repr__(self):
        occasion = self.occasion if self.occasion else "N/A"
        season = self.season if self.season else "N/A"
        return (
            f"Outfit(id={self.outfit_id}, "
            f"occasion={occasion}, "
            f"season={season}, "
            f"items_count={len(self.items) if self.items else 0})"
        )
