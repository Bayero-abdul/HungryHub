#!/usr/bin/python3
"""
This module contains a ``BaseModel`` class that defines \
all common attributes/methods for other classes.
"""

import uuid
import sqlalchemy
import models
from datetime import datetime
from os import getenv
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """defines all commom attributes/methods for other classes."""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

            if kwargs.get("created_at", None) and isinstance(
                    self.created_at, str):
                self.created_at = datetime.fromisoformat(kwargs["created_at"])
            else:
                self.created_at = datetime.utcnow()

            if kwargs.get("updated_at", None) and isinstance(
                    self.updated_at, str):
                self.updated_at = datetime.fromisoformat(kwargs["updated_at"])
            else:
                self.updated_at = datetime.utcnow()

            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """string representaion of the instances."""
        return ("[{}] ({}) {}".format(type(self).__name__, self.id,
                                      self.__dict__))

    def save(self):
        """Updates the updated_at date."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_fs=None):
        """returns a dictionary containing all keys/values of \
         __dict__ of the instance."""
        from copy import deepcopy
        new_dict = deepcopy(self.__dict__)
        new_dict['__class__'] = self.__class__.__name__
        for key in self.__dict__:
            if key in ("created_at", "updated_at"):
                value = self.__dict__[key].isoformat()
                new_dict[key] = value
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
