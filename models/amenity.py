#!/usr/bin/python3
""" The Amenity Module for the project """
from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    '''amenity class for the project'''
    __tablename__ = 'amenities'
    if storage_type == 'db':
        """ for db storage """
        name = Column(String(128), nullable=False)
    else:
        """ for file storage """
        name = ""
