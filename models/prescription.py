#!/usr/bin/python
""" holds class Prescription"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class Prescription(BaseModel, Base):
    """Representation of Prescription """
    if models.storage_t == 'db':
        __tablename__ = 'prescriptions'
        hospital_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        doctor_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        hospital_id = ""
        doctor_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """initializes Prescription"""
        super().__init__(*args, **kwargs)
