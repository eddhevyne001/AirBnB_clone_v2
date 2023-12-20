#!/usr/bin/python3
""" The city Module """
from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ This is the city class """
    __tablename__ = 'cities'
    if storage_type == 'db':
        """ Database Storage Columns """
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship('Place', backref='cities',
                              cascade='all, delete, delete-orphan')
    else:
        """ File Storage Columns """
        name = ''
        state_id = ''
