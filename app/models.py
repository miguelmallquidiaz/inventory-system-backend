from sqlalchemy import Column, Integer, Numeric, String, Boolean, ForeignKey, DATE
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .database import Base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255))
    name = Column(String(20), nullable=False)
    first_surname = Column(String(20), nullable=False)
    second_last_name = Column(String(20), nullable=False)
    phone = Column(String(9), nullable=False)
    role = Column(String(10), nullable=False, default='employee')

# Category Table
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship with Subcategories
    subcategories = relationship("Subcategory", back_populates="category")

# Client Table
class Client(Base):
    __tablename__ = 'clients'
    dni = Column(String(8), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    phone = Column(String(9), nullable=False)
    address = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False, unique=True, index=True)

    # Relationship with Reservations
    reservations = relationship("Reservation", back_populates="client")

# Subcategory Table
class Subcategory(Base):
    __tablename__ = 'subcategories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    measures = Column(String(100), nullable=False)  # Example: Liters, Kilograms, Doses, etc.
    is_active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    # Relationship with Category
    category = relationship("Category", back_populates="subcategories")

    # Relationship with Products
    products = relationship("Product", back_populates="subcategory")

# Product Table
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    total_stock = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True)
    subcategory_id = Column(Integer, ForeignKey('subcategories.id'), nullable=False)
    
    # Relationship with Subcategory
    subcategory = relationship("Subcategory", back_populates="products")

class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_date = Column(DATE, nullable=False)
    delivery_date = Column(DATE, nullable=False)
    reservation_status = Column(String(10), nullable=False, default='pending')  # Example: pending, completed
    client_dni = Column(String(8), ForeignKey('clients.dni'), nullable=False)

    # Relationship with Client
    client = relationship("Client", back_populates="reservations")
    
    # Relationship with ReservationItem
    items = relationship("ReservationItem", back_populates="reservation")

class ReservationItem(Base):
    __tablename__ = 'reservation_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_id = Column(Integer, ForeignKey('reservations.id'), nullable=False)
    product_code = Column(Integer, ForeignKey('products.id'), nullable=False)  # Reference to Product
    quantity = Column(Integer, nullable=False)

    # Relationship with Reservation
    reservation = relationship("Reservation", back_populates="items")
    
    # Relationship with Product
    product = relationship("Product")