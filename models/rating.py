#!/usr/bin/python3
"""This module contains the `Rating class`.
"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Rating(BaseModel, Base):
    """Rating Table"""

    if models.storage_t == "db":
        __tablename__ = "ratings"
        food_id = Column(String(60), ForeignKey('foods.id'), nullable=False)
        rating = Column(Float, nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        restaurant_id = Column(
            String(60),
            ForeignKey('restaurants.id'),
            nullable=False)

    else:
        food_id = ""
        rating = ""
        user_id = ""
        restaurant_id = ""

    def __init__(self, *args, **kwargs):
        """initializes Rating"""
        super().__init__(*args, **kwargs)
