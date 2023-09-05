#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.storage import db_storage
from models.hospital import Hospital
from models.base_model import BaseModel
from models.prescription import Prescription
from models.patient import Patient
from models.doctor import Doctor
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Doctor": Doctor, "Hospital": Hospital, "Base_model": Base_model,
           "Prescription": Prescription, "Patient": Patient}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/storage/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/storage/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_storage/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    def test_new(self):
        """test that new adds an object to the database"""

    def test_save(self):
        """Test that save properly saves objects to file.json"""

    def test_get(self):
        """test that get returns an object of a given class by id."""
        storage = models.storage
        obj = Hospital(name='Flynn')
        obj.save()
        self.assertEqual(obj.id, storage.get(Hospital, obj.id).id)
        self.assertEqual(obj.name, storage.get(Hospital, obj.id).name)
        self.assertIsNot(obj, storage.get(Hospital, obj.id + 'op'))
        self.assertIsNone(storage.get(Hospital, obj.id + 'op'))
        self.assertIsNone(storage.get(Hospital, 45))
        self.assertIsNone(storage.get(None, obj.id))
        self.assertIsNone(storage.get(int, obj.id))
        with self.assertRaises(TypeError):
            storage.get(Hospital, obj.id, 'op')
        with self.assertRaises(TypeError):
            storage.get(Hospital)
        with self.assertRaises(TypeError):
            storage.get()

    def test_count(self):
        """test that count returns the number of objects of a given class."""
        storage = models.storage
        self.assertIs(type(storage.count()), int)
        self.assertIs(type(storage.count(None)), int)
        self.assertIs(type(storage.count(int)), int)
        self.assertIs(type(storage.count(Hospital)), int)
        self.assertEqual(storage.count(), storage.count(None))
        Hospital(name='Radiant').save()
        self.assertGreater(storage.count(Hospital), 0)
        self.assertEqual(storage.count(), storage.count(None))
        a = storage.count(Hospital)
        State(name='Nairobi Womens').save()
        self.assertGreater(storage.count(Hospital), a)
        Doctor(name='Godfrey').save()
        self.assertGreater(storage.count(), storage.count(Hospital))
        with self.assertRaises(TypeError):
            storage.count(Hospital, 'op')
