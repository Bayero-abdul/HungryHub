#!/usr/bin/python3
"""This module contains the `Address class`.
"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Address(BaseModel, Base):
    """Address Table"""

    if models.storage_t == "db":
        __tablename__ = "addresses"
        street = Column(String(256), nullable=False)
        city = Column(String(128), nullable=False)
        state = Column(String(128), nullable=True)
        postal_code = Column(String(20), nullable=False)
        country = Column(String(128), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=True)
        restaurant_id = Column(
            String(60),
            ForeignKey('restaurants.id'),
            nullable=True)

        orders = relationship("Order", backref="address")
    else:
        street = ""
        city = ""
        state = ""
        postal_code = ""
        country = ""
        user_id = ""
        restaurant_id = ""

    def __init__(self, *args, **kwargs):
        """initializes Address"""
        super().__init__(*args, **kwargs)
