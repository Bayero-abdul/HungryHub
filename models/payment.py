#!/usr/bin/python3
"""This module contains the `Payment class`.
"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Payment(BaseModel, Base):
    """Payment Table"""

    if models.storage_t == "db":
        __tablename__ = "payments"
        amount = Column(Integer, nullable=False, default=0)
        payment_status = Column(String(128), nullable=True)
        payment_method = Column(String(128), nullable=True)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)

    else:
        amount = 0
        payment_status = ""
        payment_method = ""
        user_id = ""
        order_id = ""

    def __init__(self, *args, **kwargs):
        """initializes Payment"""
        super().__init__(*args, **kwargs)
