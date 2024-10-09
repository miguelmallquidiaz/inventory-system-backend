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