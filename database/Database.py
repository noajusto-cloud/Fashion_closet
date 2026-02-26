import sqlite3
from datetime import date
from tabulate import tabulate

class Database:
    def __init__(self, db_name="wardrobe.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Garments (
                item_id INTEGER PRIMARY KEY,
                category TEXT,
                color TEXT,
                season TEXT,
                brand TEXT,
                price REAL,
                last_worn DATE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Outfits (
                outfit_id INTEGER PRIMARY KEY,
                season TEXT,
                occasion TEXT
            )
        ''')

        # many-to-many table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Outfit_Items (
                outfit_id INTEGER,
                garment_id INTEGER,
                FOREIGN KEY(outfit_id) REFERENCES Outfits(outfit_id),
                FOREIGN KEY(garment_id) REFERENCES Garments(item_id),
                PRIMARY KEY(outfit_id, garment_id)
            )
        ''')

        self.conn.commit()
    #Add new item and return his ID
    def add_item(self, category, color, season, brand, price):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Garments (category, color, season, brand, price, last_worn) VALUES (?, ?, ?, ?, ?, ?)",
                (category, color, season, brand, price, None)
            )
            return cursor.lastrowid

    #Update Item
    def update_item(self, item_id, **kwargs):
        fields = ", ".join(f"{k}=?" for k in kwargs)
        values = list(kwargs.values()) + [item_id]
        with self.conn:
            self.conn.execute(f"UPDATE Garments SET {fields} WHERE item_id=?", values)
    
    #Remove Item By ID
    def remove_item(self, item_id):
        with self.conn:
            self.conn.execute("DELETE FROM Garments WHERE item_id=?", (item_id,))
            self.conn.execute("DELETE FROM Outfit_Items WHERE garment_id=?", (item_id,))

    #Get all items
    def get_all_items(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Garments")
        return cursor.fetchall()

    def get_unused_items(self, days=30):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM Garments WHERE last_worn IS NULL OR DATE(last_worn) <= DATE('now', ? || ' days')",
            (-days,)
        )
        return cursor.fetchall()

    def mark_item_as_worn(self, item_id):
        today = date.today()
        with self.conn:
            self.conn.execute(
                "UPDATE Garments SET last_worn=? WHERE item_id=?",
                (today, item_id)
            )

    def add_outfit(self, season, occasion, garment_ids=None):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Outfits (season, occasion) VALUES (?, ?)",
                (season, occasion)
            )
            outfit_id = cursor.lastrowid

            if garment_ids:
                for gid in garment_ids:
                    cursor.execute(
                        "INSERT INTO Outfit_Items (outfit_id, garment_id) VALUES (?, ?)",
                        (outfit_id, gid)
                    )
            return outfit_id

    def get_all_outfits(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Outfits")
        outfits = cursor.fetchall()
        result = []
        for o in outfits:
            outfit_id = o[0]
            cursor.execute(
                "SELECT garment_id FROM Outfit_Items WHERE outfit_id=?",
                (outfit_id,)
            )
            items = [row[0] for row in cursor.fetchall()]
            result.append({
                "id": o[0],
                "season": o[1],
                "occasion": o[2],
                "garment_ids": items
            })
        return result

    # Delete outfit 
    def remove_outfit(self, outfit_id):
        with self.conn:
            self.conn.execute("DELETE FROM Outfits WHERE outfit_id=?", (outfit_id,))
            self.conn.execute("DELETE FROM Outfit_Items WHERE outfit_id=?", (outfit_id,))

    def mark_outfit_as_worn(self, outfit_id):
        today = date.today()
        cursor = self.conn.cursor()
        cursor.execute("SELECT garment_id FROM Outfit_Items WHERE outfit_id=?", (outfit_id,))
        garment_ids = [row[0] for row in cursor.fetchall()]
        with self.conn:
            for gid in garment_ids:
                self.conn.execute(
                    "UPDATE Garments SET last_worn=? WHERE item_id=?",
                    (today, gid)
                )
