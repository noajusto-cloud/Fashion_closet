import sys
from database.Database import *
from Models.Garment import *
from Models.Outfit import *
from Models.Stylish_Model import *
from AI_server.Ollama_Client import *
from Views.cli_view import *

class Main_Controller:
    def __init__(self):
        self.db = Database()
        self.view = CLI_View()
        self.model = Stylist_Model(self.db) 
        self.ai_server = Ollama_Client()
    def run(self):
        self.view.display_welcome()
        while True:
            self.view.display_menu()
            choice = self.view.get_user_choice()

            if choice == '1':
                self.add_new_garment()
            elif choice == '2':
                self.remove_garment()    
            elif choice == '3':
                self.show_all_items()
            elif choice == '4':
                self.create_outfit()
            elif choice == '5':
                self.show_unused_items()
            elif choice == '6':
                user_query = self.view.get_ai_query() 
                if user_query:
                    self.view.display_ai_thinking()
                    wardrobe_context = self.model.get_inventory_string() 
                    full_prompt = f"Wardrobe: {wardrobe_context}. Question: {user_query}. Respond in English."
                    response = self.ai_server.ask_ollama(full_prompt)
                    self.view.display_ai_response(response)
            elif choice == '7':
                self.update_garment()
            elif choice == '8':
                self.mark_garment_flow()
            elif choice == '9':
                self.view.display_message("Exiting... Stay stylish!")
                sys.exit()
            else:
                self.view.display_message("Invalid choice, please try again.")

    # ----------------- Garment Logic -----------------
    def add_new_garment(self):
        data = self.view.get_garment_input()
        if data:
            category, color, season, brand, price = data
            self.db.add_item(category, color, season, brand, price)
            self.view.display_message(f"Successfully added {color} {category} to your closet!")
        else:
            self.view.display_message("Action canceled.")

    def remove_garment(self):
        item_id = self.view.get_mark_item_as_worn_input()
        self.db.remove_item(item_id)
        self.view.display_message(f"Garment ID {item_id} successfullt removed.") 


    def get_all_garments_objects(self):
        items_data = self.db.get_all_items()
        return [Garment(*data) for data in items_data]

    def show_all_items(self):
        items = self.get_all_garments_objects()
        self.view.display_garments(items)

    # ----------------- Outfit Logic -----------------
    def create_outfit(self):
        items = self.get_all_garments_objects()
        data = self.view.get_outfit_input(items)

        if data:
            season, occasion, garment_ids = data
            outfit_id = self.db.add_outfit(season, occasion, garment_ids)

            # Mechanism: creating an outfit means the selected garments were worn today
            for gid in garment_ids:
                self.db.mark_item_as_worn(gid)

            self.view.display_message(
                f"Outfit #{outfit_id} created successfully! Marked {len(garment_ids)} garment(s) as worn today."
            )
        else:
            self.view.display_message("Outfit creation canceled.")

    # ----------------- Unused Items -----------------
    def show_unused_items(self, days=30):
        unused_data = self.db.get_unused_items(days)
        self.view.display_unused_items(unused_data, days)

    # ----------------- Update Garment -----------------
    def update_garment(self):
        data = self.view.get_update_garment_input()
        if not data:
            self.view.display_message("Update canceled.")
            return

        item_id, fields = data
        self.db.update_item(item_id, **fields)
        self.view.display_message(f"Garment ID {item_id} updated successfully.")

    # ----------------- Mark Items as Worn -----------------
    def mark_item_as_worn(self, item_id):
        self.db.mark_item_as_worn(item_id)
        self.view.display_message(f"Garment ID {item_id} marked as worn today.")

    def mark_garment_flow(self):
        item_id = self.view.get_mark_item_as_worn_input()
        if item_id is None:
            self.view.display_message("Action canceled.")
            return
        self.mark_item_as_worn(item_id)


