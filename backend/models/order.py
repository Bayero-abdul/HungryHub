#!/usr/bin/python3
"""This module contains the `Order class`.
"""

import models
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Order(BaseModel, Base):
    """Order Table"""
    if models.storage_t == "db":
        __tablename__ = "orders"
        total_price = Column(Integer, nullable=False, default=0)
        total_quantity = Column(Integer, nullable=False, default=0)
        date_created = Column(DateTime, nullable=True)
        date_fulfilled = Column(DateTime, nullable=True)
        order_status = Column(String(128), nullable=True)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        address_id = Column(
            String(60),
            ForeignKey('addresses.id'),
            nullable=False)
        restaurant_id = Column(
            String(60),
            ForeignKey('restaurants.id'),
            nullable=False)

        payment = relationship("Payment", backref="order")

    else:
        total_price = 0
        total_quantity = 0
        date_created = ""
        date_fulfilled = ""
        order_status = ""
        user_id = ""
        address_id = ""
        restaurant_id = ""

    def __init__(self, *args, **kwargs):
        """initializes Order"""
        super().__init__(*args, **kwargs)
