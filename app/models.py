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
    role = Column(String(10), nullable=False, default='employee')

# Category Table
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship with Subcategories
    subcategories = relationship("Subcategory", back_populates="category")

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

    # Relationship with ReservationItem
    reservation_items = relationship("ReservationItem", back_populates="product")

class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_date = Column(DATE, nullable=False)
    delivery_date = Column(DATE, nullable=False)
    client_dni = Column(String(8), nullable=False)
    reservation_status = Column(String(10), nullable=False, default='pending')  # Example: pending, completed

    # Relationship with ReservationItem
    items = relationship("ReservationItem", back_populates="reservation")

class ReservationItem(Base):
    __tablename__ = 'reservation_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_id = Column(Integer, ForeignKey('reservations.id'), nullable=False)
    product_code = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relationship with Reservation
    reservation = relationship("Reservation", back_populates="items")
    
    # Relationship with Product
    product = relationship("Product", back_populates="reservation_items")