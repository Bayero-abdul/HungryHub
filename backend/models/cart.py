#!/usr/bin/python3
"""This module contains the `Cart and CartItem class`.
"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Cart(BaseModel, Base):
    """Cart Table"""

    if models.storage_t == "db":
        __tablename__ = "carts"
        total_price = Column(Integer, nullable=False, default=0)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

        cart_items = relationship("CartItem", backref="cart")
    else:
        total_price = 0
        user_id = ""

    def __init__(self, *args, **kwargs):
        """initializes Cart"""
        super().__init__(*args, **kwargs)


class CartItem(BaseModel, Base):
    """Cart Item Table"""

    if models.storage_t == "db":
        __tablename__ = "cart_items"
        food_id = Column(String(60), ForeignKey('foods.id'), nullable=False)
        quantity = Column(Integer, nullable=False, default=0)
        cart_id = Column(String(60), ForeignKey('carts.id'), nullable=False)
    else:
        food_id = ""
        quantity = 0
        cart_id = ""

    def __init__(self, *args, **kwargs):
        """initializes CartItem"""
        super().__init__(*args, **kwargs)
