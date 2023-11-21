import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Tests for the BaseModel class"""

    def test_init(self):
        """Tests the __init__ method of the BaseModel class"""
        # Test that an instance of BaseModel is created
        bm = BaseModel()
        self.assertIsInstance(bm, BaseModel)

        # Test that the id attribute is a string
        self.assertIsInstance(bm.id, str)

        # created_at and updated_at attributes are datetime objects
        self.assertIsInstance(bm.created_at, datetime)
        self.assertIsInstance(bm.updated_at, datetime)

    def test_str(self):
        """Tests the __str__ method of the BaseModel class"""
        bm = BaseModel()
        expected_dict = bm.__dict__
        actual_str = str(bm)
        # Extract the dictionary from the actual string representation
        actual_dict_str = actual_str[actual_str.find("{"):
                                     actual_str.rfind("}") + 1]
        actual_dict = json.loads(
            actual_dict_str.replace("'", '"').replace(
                "datetime.datetime", '"datetime.datetime"'))
        self.assertDictEqual(actual_dict, expected_dict)

    def test_save(self):
        """Tests the save method of the BaseModel class"""
        bm = BaseModel()
        old_updated_at = bm.updated_at
        bm.save()
        new_updated_at = bm.updated_at

        # Test that the updated_at attribute was updated
        self.assertNotEqual(old_updated_at, new_updated_at)

    def test_to_dict(self):
        """Tests the to_dict method of the BaseModel class"""
        bm = BaseModel()
        bm_dict = bm.to_dict()

        # Test that the returned value is a dictionary
        self.assertIsInstance(bm_dict, dict)

        # Test that the dictionary contains the expected keys and values
        self.assertEqual(bm_dict["id"], bm.id)
        self.assertEqual(bm_dict["created_at"], bm.created_at)
        self.assertEqual(bm_dict["__class__"], "BaseModel")
        self.assertEqual(bm_dict["updated_at"], bm.updated_at)


if __name__ == '__main__':
    unittest.main()