#!/usr/bin/python3
"""This module contains the `Food class`.
"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Food(BaseModel, Base):
    """Food Table"""

    if models.storage_t == "db":
        __tablename__ = "foods"
        name = Column(String(128), nullable=False)
        description = Column(String(512), nullable=True)
        available_quantity = Column(Integer, nullable=False, default=0)
        price = Column(Integer, nullable=False, default=0)
        image_url = Column(String(512), nullable=True)
        restaurant_id = Column(
            String(60),
            ForeignKey('restaurants.id'),
            nullable=False)
    else:
        name = ""
        description = ""
        available_quantity = 0
        price = 0
        image_url = ""
        restaurant_id = ""

    def __init__(self, *args, **kwargs):
        """initializes Food"""
        super().__init__(*args, **kwargs)
