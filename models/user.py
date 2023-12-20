#!/usr/bin/python3
"""This script creates a user class"""
from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Class for the User Object"""
    __tablename__ = 'users'
    if storage_type == 'db':
        """ DB Storage Columns """
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship('Place', backref='user',
                              cascade='all, delete, delete-orphan')
        reviews = relationship('Review', backref='user',
                               cascade='all, delete, delete-orphan')
    else:
        """ File Storage Columns """
        email = ""
        password = ""
        first_name = ""
        last_name = ""
