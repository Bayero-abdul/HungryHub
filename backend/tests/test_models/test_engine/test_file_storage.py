#!/usr/bin/python3
"""Module contains tests for file storage.
"""

import unittest
import os
import json
from datetime import datetime
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Tests for the FileStorage class."""

    def setUp(self):
        """Code to execute before testing each test"""

        self.fs = FileStorage()

    def tearDown(self):
        """Code to execute after eavh test are executed"""

        if os.path.exists("file.json"):
            os.remove("file.json")

        FileStorage._FileStorage__objects = {}

    def test_IsFileStorage(self):
        """test for instances of FileStorage."""

        self.assertIsInstance(FileStorage(), FileStorage)

    def test_has_file_path_attr(self):
        """test if private class attribute __file_path
        exits."""

        self.assertTrue(hasattr(FileStorage(), '_FileStorage__file_path'))
        self.assertFalse(hasattr(FileStorage(), '__file_path'))

        with self.assertRaises(TypeError):
            self.fs._FileStorage__file_path()

    def test_has_objects_attr(self):
        """test if private class attribute __objects exists."""

        self.assertTrue(hasattr(FileStorage(), '_FileStorage__objects'))
        self.assertFalse(hasattr(FileStorage(), '__objects'))
        self.assertIs(type(self.fs._FileStorage__objects), dict)
        print(self.fs._FileStorage__objects)
        self.assertTrue(self.fs._FileStorage__objects == {})

        with self.assertRaises(TypeError):
            self.fs._FileStorage__objects()

    def test_all(self):
        """test if all() returns a dictionary"""

        self.assertTrue(hasattr(self.fs, 'all'))
        self.assertIsInstance(self.fs.all(), dict)
        self.assertTrue(self.fs._FileStorage__objects == {})


    def test_new(self):
        """test for new() function."""

        self.assertTrue(hasattr(self.fs, 'new'))
        my_model = BaseModel()
        storage.new(my_model)
        self.assertIn("BaseModel." + my_model.id, storage.all().keys())
        self.assertTrue(dir(my_model) == dir(BaseModel()))

        with self.assertRaises(AttributeError):
            types = [1, 'string', [34, 6], {'hello': 7}, (3, 6), True, None]
            for t in types:
                self.fs.new(t)

        with self.assertRaises(TypeError):
            storage.new(my_model, 45)

    def test_save(self):
        """test for save() function."""

        my_model = BaseModel()
        b_updated_at = my_model.updated_at
        my_model.save()
        self.assertTrue(b_updated_at != my_model.updated_at)
        self.assertTrue(hasattr(self.fs, 'save'))

        """test if __file_path exists"""
        self.assertTrue(os.path.exists('file.json'))

        with self.assertRaises(TypeError):
            self.fs.save(1)

    def test_reload(self):
        """test for reload()."""

        self.assertTrue(hasattr(self.fs, 'reload'))
        my_model = BaseModel()
        my_model.save()
        test_dict = {}
        with open('file.json', 'r', encoding='utf-8') as f:
            read = json.loads(f.read())
            for key, value in read.items():
                test_dict[key] = BaseModel(**value).to_dict()

        self.fs.reload()
        store_dict = {}
        for key, value in self.fs._FileStorage__objects.items():
            store_dict[key] = value.to_dict()

        self.assertTrue(test_dict == store_dict)

        with self.assertRaises(TypeError):
            self.fs.reload(None)


if __name__ == "__main__":
    unittest.main()
