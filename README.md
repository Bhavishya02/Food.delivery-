# Food Delivery

## Overview
This is a **Food delivery project** built with **FastAPI** and **SQLite**, designed to handle user authentication, restaurant management, orders, and delivery assignments. The API provides endpoints for users to place orders, restaurants to manage menus, and riders to handle deliveries efficiently.

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
### ** Clone the Repository**
```bash
git clone https://github.com/your-username/food-delivery-api.git
cd food-delivery
```

### ** Create & Activate Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows
```

### ** Install Dependencies**
```bash
pip install -r requirements.txt
```
### ** Start the Server**
```bash
uvicorn main:app --reload
```

### **Run streamlit frontend**
```bash
streamlit run frontend.py
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


### **Orders & Delivery**
- **Place Order:** `POST /place_order`
- **Update Rider Location:** `PUT /update_rider_location/{rider_id}`


## Contributing
Feel free to contribute by creating a pull request or raising an issue.



