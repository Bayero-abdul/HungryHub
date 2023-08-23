#!/usr/bin/python3
"""this module contain ``FileStorage`` class that serializes \
instances to a JSON file and deserializes JSON file to instances.
"""

import json
import os.path
import models
from models.base_model import BaseModel
from models.user import User
from models.restaurant import Restaurant
from models.address import Address
from models.food import Food
from models.order import Order
from models.cart import Cart
from models.cart import CartItem
from models.rating import Rating
from models.payment import Payment


classes = {'BaseModel': BaseModel,
           'User': User,
           'Restaurant': Restaurant,
           'Address': Address,
           'Food': Food,
           'Order': Order,
           'Cart': Cart,
           'CartItem': CartItem,
           'Payment': Payment,
           'Rating': Rating
}


class FileStorage:
    """serializes instances to a JSON file and deserializes \
JSON file to instances."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        class_name = obj.__class__.__name__
        key = class_name + "." + obj.id
        type(self).__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file"""
        with open(type(self).__file_path, "w", encoding="utf-8") as f:
            store_dict = {}
            for key, value in type(self).__objects.items():
                store_dict[key] = value.to_dict()
            f.write(json.dumps(store_dict))

    def reload(self):
        """deserializes the JSON file to __objects"""
        if os.path.exists(self.__file_path):
            with open(type(self).__file_path, "r", encoding="utf-8") as f:
                read = json.loads(f.read())
                for k, val in read.items():
                    type(self).__objects[k] = eval(val['__class__'])(**val)

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(cls).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
