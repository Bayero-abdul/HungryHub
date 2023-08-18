#!/usr/bin/python3
"""This module contains the `Restaurant class`.
"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Restaurant(BaseModel, Base):
    """Restaurant that inherits from BaseModel."""

    if models.storage_t == "db":
        __tablename__ = "restaurants"
        name = Column(String(128), nullable=False)
        description = Column(String(512), nullable=True)
        logo_url = Column(String(512), nullable=True)
        contact_phone = Column(String(20), nullable=True)
        min_order_cost = Column(Integer, nullable=False, default=0)
        delivery_cost = Column(Integer, nullable=False, default=0)
        is_active = Column(Boolean, nullable=False, default=True)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

        addresses = relationship("Address", backref="restaurant")
        foods = relationship("Food", backref="restaurant")
        orders = relationship("Order", backref="restaurant")
        ratings = relationship("Rating", backref="restaurant")

    else:
        name = ""
        description = ""
        logo_url = ""
        contact_phone = ""
        min_order_cost = 0
        delivery_cost = 0
        is_active = True
        user_id = ""

    def __init__(self, *args, **kwargs):
        """initializes Restaurant"""
        super().__init__(*args, **kwargs)
