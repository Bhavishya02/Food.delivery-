from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, Session, relationship, declarative_base
import random

app = FastAPI()

DATABASE_URL = "sqlite:///./food_delivery.db"  # Replace with PostgreSQL for production
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    address = Column(String)
    password = Column(String)  # Added password field

class Rider(Base):
    __tablename__ = "riders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    is_available = Column(Integer, default=1)

class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cuisine = Column(String)
    location = Column(String)

class Menu(Base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    item_name = Column(String)
    price = Column(Float)
    restaurant = relationship("Restaurant")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    rider_id = Column(Integer, ForeignKey("riders.id"), nullable=True)
    status = Column(String, default="Pending")
    user = relationship("User")
    restaurant = relationship("Restaurant")
    rider = relationship("Rider", foreign_keys=[rider_id])

Base.metadata.create_all(bind=engine)

# Pydantic Models
class UserCreate(BaseModel):
    name: str
    address: str
    password: str

class UserLogin(BaseModel):
    name: str
    password: str

class RiderCreate(BaseModel):
    name: str
    location: str

class RestaurantCreate(BaseModel):
    name: str
    cuisine: str
    location: str

class MenuCreate(BaseModel):
    restaurant_id: int
    item_name: str
    price: float

class OrderCreate(BaseModel):
    user_id: int
    restaurant_id: int

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints

@app.post("/register_user")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    if db.query(User).filter(User.name == user.name).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    db_user = User(name=user.name, address=user.address, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user.name, User.password == user.password).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    return db_user

@app.post("/register_rider")
def register_rider(rider: RiderCreate, db: Session = Depends(get_db)):
    db_rider = Rider(name=rider.name, location=rider.location)
    db.add(db_rider)
    db.commit()
    db.refresh(db_rider)
    return db_rider

@app.post("/register_restaurant")
def register_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    db_restaurant = Restaurant(name=restaurant.name, cuisine=restaurant.cuisine, location=restaurant.location)
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@app.post("/add_menu_item")
def add_menu_item(menu: MenuCreate, db: Session = Depends(get_db)):
    db_menu = Menu(restaurant_id=menu.restaurant_id, item_name=menu.item_name, price=menu.price)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

@app.get("/suggest_restaurants/{cuisine}/{max_time}")
def suggest_restaurants(cuisine: str, max_time: int, db: Session = Depends(get_db)):
    # Partial, case-insensitive match for cuisine
    restaurants = db.query(Restaurant).filter(Restaurant.cuisine.ilike(f"%{cuisine}%")).all()
    if not restaurants:
        raise HTTPException(status_code=404, detail="No restaurants found")
    return restaurants

from fastapi.encoders import jsonable_encoder

@app.post("/place_order")
def place_order(order: OrderCreate, db: Session = Depends(get_db)):
    available_riders = db.query(Rider).filter(Rider.is_available == 1).all()
    assigned_rider = random.choice(available_riders) if available_riders else None
    db_order = Order(
        user_id=order.user_id, 
        restaurant_id=order.restaurant_id, 
        rider_id=assigned_rider.id if assigned_rider else None
    )
    if assigned_rider:
        assigned_rider.is_available = 0
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return jsonable_encoder(db_order)

@app.put("/update_rider_location/{rider_id}")
def update_rider_location(rider_id: int, location: str, db: Session = Depends(get_db)):
    rider = db.query(Rider).filter(Rider.id == rider_id).first()
    if not rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    rider.location = location
    db.commit()
    return {"message": "Rider location updated"}

@app.get("/user_order_history/{user_id}")
def user_order_history(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders

@app.get("/rider_order_history/{rider_id}")
def rider_order_history(rider_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.rider_id == rider_id, Order.status == "Completed").all()
    return orders

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
