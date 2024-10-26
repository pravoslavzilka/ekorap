from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, Date, DateTime, Float, PickleType
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from database import Base
from sqlalchemy.ext.mutable import MutableDict


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    email = Column(String(150))
    paasword = Column(String(300))

    def __init__(self, email):
        self.email = email


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    description = Column(String(2000))
    address = Column(String(300))
    Ico = Column(Integer)
    email = Column(String(150))
    paasword = Column(String(300))

    form_items = relationship("FormItem", back_populates="user")



    def __init__(self, name, description, address):
        self.name = name
        self.description = description
        self.address = address


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class FormItem(Base):
    __tablename__ = "formitems"
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    count = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="form_items", foreign_keys=[user_id])

    def __init__(self, name, count):
        self.name = name
        self.count = count



class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(300))

    def __init__(self, name):
        self.name = name