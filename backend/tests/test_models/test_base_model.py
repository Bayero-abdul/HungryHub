#!/usr/bin/python3
"""Test for the base_model.py.
"""

import os
import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """TestCase for the BaseModel Class."""

    def setUp(self):
        """the set-up code."""

        self.my_model = BaseModel()
        self.my_model.name = "My First Model"
        self.my_model.my_number = 89

    def test_isBaseModel(self):
        """test for instances of BaseModel"""

        self.assertIs(type(self.my_model), BaseModel)

    def test_idtype(self):
        """test if id is of string type."""

        self.assertIs(type(self.my_model.id), str)

    def test_typecreated_at(self):
        """test if created_at is of datetime type"""

        self.assertIs(type(self.my_model.created_at), datetime)

    def test_typeupdated_at(self):
        """test if updated_at is of datetime type"""

        self.assertIs(type(self.my_model.updated_at), datetime)

    def test_save(self):
        """test the save() method."""

        updated_at_before_save = self.my_model.updated_at
        self.my_model.save()
        self.assertTrue(updated_at_before_save != self.my_model.updated_at)

        self.assertTrue(os.path.exists('file.json'))

    def test_to_dict(self):
        """Test if to_dict() returns a dictionary."""

        my_model_json = self.my_model.to_dict()
        self.assertIs(type(my_model_json), dict)

    def test__str__(self):
        """Test for the string representation."""

        self.assertEqual(str(self.my_model), "[BaseModel] ({}) {}"
                         .format(self.my_model.id, self.my_model.__dict__))

    def test_to_dict_has_class_attr(self):
        """Test if to_dict() has __class__ attribute."""

        my_model_json = self.my_model.to_dict()
        self.assertTrue(hasattr(my_model_json, '__class__'))

    def test_to_dict_output(self):
        """Test to_dict output."""

        b = BaseModel()
        dt = datetime.now()
        b.id = "12345"
        b.created_at = b.updated_at = dt
        test_dict = {
            'id': "12345",
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
            '__class__': 'BaseModel'
        }
        self.assertDictEqual(test_dict, b.to_dict())

    def test_uniqueid(self):
        """Test if id of different instances is different."""

        my_model_1 = BaseModel()
        self.assertTrue(my_model_1.id != self.my_model.id)


if __name__ == "__main__":
    unittest.main()
