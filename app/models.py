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