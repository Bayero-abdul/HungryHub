#!/usr/bin/python3
"""The module contains `user class`.
"""


import models
import sqlalchemy
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """User that inherits from BaseModel."""
    if models.storage_t == "db":
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        phone_number = Column(String(128), nullable=True)
        role = Column(String(128), nullable=True)
        profile_picture_url = Column(String(512), nullable=True)

        addresses = relationship("Address", backref="user")
        cart = relationship("Cart", backref="user")
        orders = relationship("Order", backref="user")
        payments = relationship("Payment", backref="user")
        restaurants = relationship("Restaurant", backref="user")
        ratings = relationship("Rating", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
        phone_number = ""
        role = ""
        profile_picture_url = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        if not self.email:
            self.email = ""
        if not self.password:
            self.password = ""

    """def __setattr__(self, name, value):
        sets a password with md5 encryption
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value"""
