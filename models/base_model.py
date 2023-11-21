#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """ BaseModel class that defines all common methods for other classes """
    def __init__(self, *args, **kwargs):
        """ Initialization of the BaseModel class """
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.now()
        models.storage.new(self)

        for key, value in kwargs.items():
            if key == "__class__":
                continue
            if key in ["created_at", "updated_at"]:
                value = datetime.fromisoformat(value)
            setattr(self, key, value)

    def save(self):
        """
        Updates the public instance attribute updated_at with the current
        datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ Returns a dictionary containing all keys/values of __dict__ of the
        instance """
        dict1 = {
            **self.__dict__,
            'created_at': self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            'updated_at': self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            '__class__': self.__class__.__name__
        }
        return dict1

    def __str__(self):
        """ Prints a string representation """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
