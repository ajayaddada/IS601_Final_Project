from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import sqlite3
import time

app = FastAPI()

def db_connection():
    return sqlite3.connect("db.sqlite", check_same_thread=False)

class Item(BaseModel):
    name: str
    price: float

class Customer(BaseModel):
    name: str
    phone: int

class Order(BaseModel):
    id: int
    customer_id: int
    notes: str


@app.post("/items")
def create_item(item: Item):
    try:
        db = db_connection()
        cur = db.cursor()
        cur.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
        db.commit()
        return {"id": cur.lastrowid, "name": item.name, "price": item.price}
    except Exception as error:
        print("ERROR:", str(error))
        raise HTTPException(status_code=500, detail="Failed to add item")
    finally:
        db.close()

@app.get("/items/{item_id}")
def get_item(item_id: int):
    db = db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    data = cur.fetchone()
    db.close()
    if not data:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": data[0], "name": data[1], "price": data[2]}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    db = db_connection()
    cur = db.cursor()
    cur.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (item.name, item.price, item_id))
    db.commit()
    db.close()
    return {"id": item_id, "name": item.name, "price": item.price}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    db = db_connection()
    cur = db.cursor()
    cur.execute("DELETE FROM items WHERE id = ?", (item_id,))
    db.commit()
    db.close()
    return {"message": f"Deleted item {item_id}"}


@app.post("/customer")
def add_customer(customer: Customer):
    db = db_connection()
    cur = db.cursor()
    cur.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
    db.commit()
    customer_id = cur.lastrowid
    db.close()
    return {"id": customer_id, "name": customer.name, "phone": customer.phone}

@app.get("/customers/{customer_id}")
def fetch_customer(customer_id: int):
    db = db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    row = cur.fetchone()
    db.close()
    if not row:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"id": row[0], "name": row[1], "phone": row[2]}

@app.put("/customers/{customer_id}")
def edit_customer(customer_id: int, customer: Customer):
    db = db_connection()
    cur = db.cursor()
    cur.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", (customer.name, customer.phone, customer_id))
    db.commit()
    db.close()
    return {"id": customer_id, "name": customer.name, "phone": customer.phone}

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    db = db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
    if cur.fetchone():
        db.close()
        return {"message": "Cannot delete. Remove customer orders first."}
    cur.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    db.commit()
    db.close()
    return {"message": "Customer deleted"}


@app.post("/orders/{order_id}")
def add_order(order: Order):
    db = db_connection()
    cur = db.cursor()
    now = int(time.time())
    cur.execute("INSERT INTO orders (timestamp, customer_id, notes) VALUES (?, ?, ?)",
                (now, order.customer_id, order.notes))
    db.commit()
    new_order_id = cur.lastrowid
    db.close()
    return {"id": new_order_id, "timestamp": now, "customer_id": order.customer_id, "notes": order.notes}

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    db = db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    result = cur.fetchone()
    db.close()
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"id": result[0], "timestamp": result[1], "customer_id": result[2], "notes": result[3]}

@app.put("/orders/{order_id}")
def update_order(order_id: int, order: Order):
    db = db_connection()
    cur = db.cursor()
    current_time = int(time.time())
    cur.execute("UPDATE orders SET timestamp = ?, customer_id = ?, notes = ? WHERE id = ?",
                (current_time, order.customer_id, order.notes, order_id))
    db.commit()
    db.close()
    return {"id": order_id, "timestamp": current_time, "customer_id": order.customer_id, "notes": order.notes}

@app.delete("/orders/{order_id}")
def remove_order(order_id: int):
    db = db_connection()
    cur = db.cursor()
    cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    db.commit()
    db.close()
    return {"message": f"Order {order_id} removed"}


@app.get("/")
def root_redirect():
    return RedirectResponse(url="/docs")
