#!/usr/bin/python3
""" File storage module """
import models
from models.base_model import BaseModel
import json


class FileStorage:
    """ Class FileStorage serves as file storage engine """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """ Returns the dictionary __objects """
        return {k: v for k, v in self.__objects.items() if cls is None or
                cls == v.__class__ or cls == v.__class__.__name__}

    def new(self, obj):
        """ Sets in __objects the obj with key <obj class name>.id"""
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """ Serializes __objects to the JSON file """
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        """ Deserializes the JSON file to __objects """
        try:
            with open(self.__file_path, 'r', encoding="utf-8") as f:
                self.__objects = {k: eval(v['__class__'])(**v)
                                  for k, v in json.load(f).items()}
        except FileNotFoundError:
            pass

    def count(self, cls):
        """ Counts the number of objects in storage """
        return sum(cls in key for key in models.storage.all().keys())
