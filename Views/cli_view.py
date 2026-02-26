from tabulate import tabulate
class CLI_View:
    def display_welcome(self):
        print("--- Welcome to your Virtual Fashion Closet ---")

    def display_menu(self):
        print("\n1. Add Garment")
        print("2. Remove Garment")
        print("3. View Closet")
        print("4. Create Outfit")
        print("5. Forgotten Items (Unused)")
        print("6. Get AI Styling Advice ✨")
        print("7. Update Garment")
        print("8. Mark Garment as Worn")
        print("9. Exit")

    def get_user_choice(self):
        return input("Select an option: ").strip()

    def get_ai_query(self):
        print("\n--- 🤖 AI Personal Stylist ---")
        return input("What is the occasion or your fashion question? ").strip()

    def display_ai_thinking(self):
        print("\nConsulting with AI Stylist (running on Docker)... Please wait.")

    def display_ai_response(self, response):
        print("\n" + "="*40)
        print("👗 STYLIST RECOMMENDATION:")
        print(response)
        print("="*40)


    def display_message(self, message):
        print(message)

    def get_garment_input(self):
        print("\n--- Add New Garment ---")
        category = input("Category (Shirt, e.g..): ").strip()
        color = input("Color: ").strip()
        season = input("Season (Summer/Winter/All): ").strip()
        brand = input("Brand: ").strip()
        try:
            price = float(input("Price: "))
            return category, color, season, brand, price
        except ValueError:
            print("Invalid price.")
            return None

    def get_update_garment_input(self):
        print("\n--- Update Garment ---")
        try:
            item_id = int(input("Enter Garment ID to update: ").strip())
        except ValueError:
            print("Invalid ID.")
            return None

        print("Leave blank to keep existing value.")
        category = input("New Category: ").strip()
        color = input("New Color: ").strip()
        season = input("New Season: ").strip()
        brand = input("New Brand: ").strip()
        price_raw = input("New Price: ").strip()

        fields = {}
        if category:
            fields["category"] = category
        if color:
            fields["color"] = color
        if season:
            fields["season"] = season
        if brand:
            fields["brand"] = brand
        if price_raw:
            try:
                fields["price"] = float(price_raw)
            except ValueError:
                print("Invalid price.")
                return None

        if not fields:
            print("No changes provided.")
            return None

        return item_id, fields

    def get_mark_item_as_worn_input(self):
        print("\n--- Mark Garment as Worn ---")
        try:
            return int(input("Enter Garment ID: ").strip())
        except ValueError:
            print("Invalid ID.")
            return None
        

    def display_garments(self, garments):
        if not garments:
            print("Your closet is empty.")
            return

        rows = []
        for g in garments:
            # DB row (tuple/list) vs model object
            if isinstance(g, (tuple, list)):
                item_id, category, color, season, brand, price, last_worn = (
                    (list(g) + [None] * 7)[:7]
                )
            else:
                item_id = getattr(g, "item_id", None)
                category = getattr(g, "category", None)
                color = getattr(g, "color", None)
                season = getattr(g, "season", None)
                brand = getattr(g, "brand", None)
                price = getattr(g, "price", None)
                last_worn = getattr(g, "last_worn", None)

            if last_worn in (None, "", "None"):
                last_worn = "Never"

            if isinstance(price, (int, float)):
                price = f"{price:.2f}"

            rows.append([item_id, category, color, season, brand, price, last_worn])

        headers = ["ID", "Category", "Color", "Season", "Brand", "Price", "Last worn"]
        print("\n--- Your Closet ---")
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def get_outfit_input(self, garments):
        print("\n--- Create New Outfit ---")
        season = input("Outfit Season: ").strip()
        occasion = input("Occasion: ").strip()

        if not garments:
            print("Your closet is empty. Add garments first!")
            return None

        print("\nSelect items to include in the outfit (comma-separated IDs):")
        for g in garments:
            print(f"{g.item_id}: {g.category} ({g.color})")

        selected_ids = input("Enter IDs: ")
        try:
            garment_ids = [int(i.strip()) for i in selected_ids.split(",") if i.strip()]
            return season, occasion, garment_ids
        except ValueError:
            print("Invalid input.")
            return None

    def display_unused_items(self, unused_data, days):
        print(f"\n--- Forgotten Items (Not worn for {days}+ days) ---")
        if not unused_data:
            print("No forgotten items!")
            return
        for item in unused_data:
            last_worn = item[6] if item[6] else "Never"
            print(f"ID: {item[0]} | {item[1]} ({item[4]}) - Last worn: {last_worn}")
