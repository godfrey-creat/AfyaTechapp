#!/usr/bin/python3
""" holds class Patient"""
import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Patient(BaseModel, Base):
    """Representation of a Patient """
    if models.storage_t == 'db':
        __tablename__ = 'patient'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        hospitals = relationship(
            "Hospital",
            cascade="all, delete, delete-orphan",
            backref="doctor"
        )
        prescriptions = relationship(
            "Prescription",
            cascade="all, delete, delete-orphan",
            backref="doctor"
        )
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def authenticate():
        #dictionary to store patients credentials securely.
        patient_credentials = {}
        patient_id = input("Enter your patient ID:")
        password = input("Enter your password")

        if patient_id in patient_credentials and patient_credentials[patient_id] == password:
            return True
        else:
            return False

    def read_prescription():
        with open("prescription_file.txt", "r") as file:
            content = file.read()
            return content
    def main():
        if authenticate():
            print("Authentication succesful!")
            prescription_content = read_prescription()
            print("prescription_file content:")
            print(prescription_file_content)
        else:
            print("Authentication Failed. Accesss denied!")

    if __name__ == "__main__":
        main()

  

    
