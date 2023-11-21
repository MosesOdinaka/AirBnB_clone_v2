#!/usr/bin/python3
""" magic method for models folder """
from models.engine.file_storage import FileStorage

storage = FileStorage().reload()
