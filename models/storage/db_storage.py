#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.hospital import Hospitals
from models.base_model import BaseModel, Base
from models.doctor import Doctor
from models.prescription import Prescription
from models.patient import Patient
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Base_model": Base_model, "Doctor": Doctor,
           "Hospital": Hospital, "Patient": Patient, "Prescription": Prescription}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        AfyaTech_MYSQL_DOCTOR = getenv('AfyaTach_MYSQL_DOCTOR')
        AfyaTech_MYSQL_PWD = getenv('AfyaTech_MYSQL_PWD')
        AfyaTech_MYSQL_HOST = getenv('AfyaTech_MYSQL_HOST')
        AfyaTech_MYSQL_DB = getenv('AfyaTech_MYSQL_DB')
        AfyaTech_ENV = getenv('AfyaTech_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(AfyaTech_MYSQL_DOCTOR,
                                             AfyaTech_MYSQL_PWD,
                                             AfyaTech_MYSQL_HOST,
                                             AfyaTech_MYSQL_DB))
        if AfyaTech_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def get(self, cls, id):
        """retrieves an object of a class with id"""
        obj = None
        if cls is not None and issubclass(cls, BaseModel):
            obj = self.__session.query(cls).filter(cls.id == id).first()
        return obj

    def count(self, cls=None):
        """retrieves the number of objects of a class or all (if cls==None)"""
        return len(self.all(cls))

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit a7ll changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
