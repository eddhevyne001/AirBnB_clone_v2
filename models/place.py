#!/usr/bin/python3
""" Place Module for HBNB project """

from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Table


if storage_type == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True,
                                 nullable=False)
                          )


class Place(BaseModel, Base):
    """ The place model """
    __tablename__ = 'places'
    if storage_type == 'db':
        """ For DB Storage, use SQL Alchemy Columns """
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review', backref='place',
                               cascade='all, delete, delete-orphan')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False, backref='place_amenities')
    else:
        """ For File Storage, python native data type """
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            ''' returns a list of reviews
            '''
            from models import storage
            all_reviews = storage.all(Review)
            output_list = []
            for single_review in all_reviews.values():
                if single_review.place_id == self.id:
                    output_list.append(single_review)
            return output_list

        @property
        def amenities(self):
            ''' input - amenity id
                Output - list of amenities
            '''
            from models import storage
            all_amenities = storage.all(Amenity)
            ourput_list = []
            for amen in all_amenities.values():
                if amen.id in self.amenity_ids:
                    ourput_list.append(amen)
            return ourput_list

        @amenities.setter
        def amenities(self, obj):
            ''' adding an Amenity.id to theattribute amenity_ids
            '''
            if obj is not None:
                if isinstance(obj, Amenity):
                    if obj.id not in self.amenity_ids:
                        self.amenity_ids.append(obj.id)
