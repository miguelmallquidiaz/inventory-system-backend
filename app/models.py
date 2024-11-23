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
    role = Column(String(7), nullable=False, default='almacen')

# Category Table
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)

    subcategories = relationship("Subcategory", back_populates="category")

# Subcategory Table
class Subcategory(Base):
    __tablename__ = 'subcategories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    measures = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    category = relationship("Category", back_populates="subcategories")
    products = relationship("Product", back_populates="subcategory")

# Product Table
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    total_stock = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    subcategory_id = Column(Integer, ForeignKey('subcategories.id'), nullable=False)
    
    subcategory = relationship("Subcategory", back_populates="products")
    product_items = relationship("OrderDetail", back_populates="product")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    delivery_date = Column(DATE, nullable=False)
    order_status = Column(String(10), nullable=False, default='pendiente')

    order_details = relationship("OrderDetail", back_populates="order")

class OrderDetail(Base):
    __tablename__ = 'order_detail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_code = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_details")
    product = relationship("Product", back_populates="product_items")