#!/usr/bin/python
"""  class Hospital"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Hospital(BaseModel, Base):
    """Representation of Hospital """
    if models.storage_t == 'db':
        __tablename__ = 'hospitals'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializing Hospital"""
        super().__init__(*args, **kwargs)
