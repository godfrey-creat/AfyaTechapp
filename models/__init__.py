#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv


storage_t = getenv("AfyaTech_TYPE_STORAGE")

if storage_t == "db":
    from models.storage.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.storage.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
