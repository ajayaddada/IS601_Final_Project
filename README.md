# Final Dosa Backend Project

This is a backend API project built using FastAPI and SQLite, to practice REST API development and relational database management. The application provides complete CRUD operations for managing a dosa restaurant's key entities.

---

## This project includes: -

- Full CRUD API for: Customers, Items and Orders.
- And also SQLite database and Auto-generated timestamps for orders
- Interactive Swagger UI at `/docs`

---

## Setup Instructions

### Step 1:
Clone the Repository
```bash
git clone https://github.com/ajayaddada/IS601_Final_Project.git
```
```bash
cd IS601-Final-Project
```
### Step 2:
Create and Activate Virtual Environment
```bash
python -m venv venv
```
For windows
```bash
venv\Scripts\activate 
```
For macOS & Linux
```bash
 source venv/bin/activate
```

### Step 3:
Install requirements
```bash
pip install -r requirements.txt
```
### Step 4:
Initialize the SQLite Database
```bash
python init_db.py
```

### Step 5:
Run the FastAPI Server
```bash
uvicorn main:app --reload
```
Once running, open http://127.0.0.1:8000/docs to explore the API.