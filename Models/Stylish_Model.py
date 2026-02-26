from database.Database import Database

class Stylist_Model:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_inventory_string(self) -> str:
        items = self.db.get_all_items()
        # items is a list of tuples: (id, category, color, season, brand, price, last_worn)
        if not items:
            return "No items in wardrobe"
        
        inventory_list = []
        for item in items:
            # item[1] is category, item[2] is color, item[4] is brand
            inventory_list.append(f"{item[2]} {item[1]} ({item[4]})")
            
        return ", ".join(inventory_list)

    def build_stylist_prompt(self, user_request: str) -> str:
        inventory = self.get_inventory_string()
        return (f"You are a professional stylist. My wardrobe has: {inventory}. "
                f"User request: {user_request}. Respond in English.")
