#!/usr/bin/python3
""" class doctor"""
import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Doctor(BaseModel, Base):
    """Representation of a doctor """
    if models.storage_t == 'db':
        __tablename__ = 'doctor'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        hospitals = relationship(
            "Hospital",
            cascade="all, delete, delete-orphan",
            backref="doctor"
        )
        prescription = relationship(
            "Prescription",
            cascade="all, delete, delete-orphan",
            backref="doctor"
        )
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes doctor"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, __name: str, __value) -> None:
        '''Sets an attribute of this class to a given value.'''
        if __name == 'password':
            if type(__value) is str:
                m = hashlib.md5(bytes(__value, 'utf-8'))
                super().__setattr__(__name, m.hexdigest())
        else:
            super().__setattr__(__name, __value)

            # doctor.py

def doctor_prescription(prescription):
    """ function that take doctor prescription and store in prescription_file.txt """
    try:
        with open('prescription_file.txt', 'a') as file:
            file.write(prescription + '\n')
        return True  # Return True if writing to file is successful
    except Exception as e:
        print(f"An error occurred: {e}")
        return False  # Return False if there was an error

