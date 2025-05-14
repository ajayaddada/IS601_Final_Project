import sqlite3
import json


connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        notes TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_id INTEGER,
        item_id INTEGER,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
    )
""")


with open("example_orders.json", "r") as file:
    order_entries = json.load(file)

for entry in order_entries:
    name, phone, timestamp, notes, items = entry["name"], entry["phone"], entry["timestamp"], entry["notes"], entry["items"]

    
    cursor.execute("SELECT id FROM customers WHERE name = ? AND phone = ?", (name, phone))
    existing = cursor.fetchone()
    customer_id = existing[0] if existing else cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone)).lastrowid

    
    order_id = cursor.execute("INSERT INTO orders (timestamp, customer_id, notes) VALUES (?, ?, ?)", (timestamp, customer_id, notes)).lastrowid

   
    for item in items:
        cursor.execute("SELECT id FROM items WHERE name = ?", (item["name"],))
        existing_item = cursor.fetchone()
        item_id = existing_item[0] if existing_item else cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item["name"], item["price"])).lastrowid
        cursor.execute("INSERT INTO order_items (order_id, item_id) VALUES (?, ?)", (order_id, item_id))

connection.commit()
connection.close()
