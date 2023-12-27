#!/usr/bin/python3
""" Base model class for AirBnB clone """
from uuid import uuid4
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Datetime

Base = declarative_base()


class BaseModel:
    """ BaseModel class that defines all common methods for other classes """
	id = Column(String(60), primary_key=True, nullable=False)
	created_at = Column(Datetime, nullable=False, default=datetime.utcnow())
	updated_at = Column(Datetime, nullable=False, default=datetime.utcnow())

	def __init__(self, *args, **kwargs):
		"""
		Initialize the BaseModel class
		"""
		self.id = str(uuid4())
		self.created_at = self.updated_at = datetime.utcnow()
		if kwargs:
			for key, value in kwargs.items():
				if key == "created_at" or key == "updated_at":
					value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
				if key != "__class__":
					setattr(self, key, value)

	def to_dict(self):
		"""
		Creates dictionary of the class and returns a dictionary of all the
		key values
		"""
		my_dict = self.__dict__.copy()
		my_dict["__class__"] = str(type(self).__name__)
		my_dict["created_at"] = self.created_at.isoformat()
		my_dict["updated_at"] = self.updated_at.isoformat()
		my_dict.pop("_sa_instance_state", None)
		return my_dict

	def __str__(self):
		"""
		Returns a string of the class, the id and the dictionary of the
		instance's attribute.
		"""
		dictn = self.__dict__.copy()
		dictn.pop("_sa_instance_state", None)
		return "[{}] ({}) {}".format(type(self).__name__, self.id, dictn)

	def save(self):
		"""
		Updates the updated_at attribute and saves the instance to storage.
		"""
		self.updated_at = datetime.utcnow()
		models.storage.new(self)
		models.storage.save()

	def delete(self):
		"""
		Deletes an instance of a class.
		"""
		models.storage.delete(self)
