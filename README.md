# Food Delivery

## Overview
This is a **Food delivery project** built with **FastAPI** and **SQLite/PostgreSQL**, designed to handle user authentication, restaurant management, orders, and delivery assignments. The API provides endpoints for users to place orders, restaurants to manage menus, and riders to handle deliveries efficiently.

## Features
- **User Authentication** (Register/Login)
- **Restaurant Management** (Add/View restaurants & menus)
- **Order Placement & Assignment** (Order food & auto-assign riders)
- **Delivery Tracking** (Rider location updates)


## Tech Stack
- **Backend:** FastAPI
- **Database:** SQLite 
- **ORM:** SQLAlchemy


## Installation & Setup
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/food-delivery-api.git
cd food-delivery
```

### **2️⃣ Create & Activate Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run Database Migrations**
```bash
python init_db.py
```

### **5️⃣ Start the Server**
```bash
uvicorn main:app --reload
```

### **6️⃣ Access API Documentation**
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints
### **User Authentication**
- **Register User:** `POST /register_user`
- **Login User:** `POST /login`

### **Restaurants & Menus**
- **Register Restaurant:** `POST /register_restaurant`
- **Add Menu Item:** `POST /add_menu_item`
- **Suggest Restaurants:** `GET /suggest_restaurants/{cuisine}/{max_time}`

### **Orders & Delivery**
- **Place Order:** `POST /place_order`
- **User Order History:** `GET /user_order_history/{user_id}`
- **Rider Order History:** `GET /rider_order_history/{rider_id}`
- **Update Rider Location:** `PUT /update_rider_location/{rider_id}`


## Contributing
Feel free to contribute by creating a pull request or raising an issue.



