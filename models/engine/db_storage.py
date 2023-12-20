#!/usr/bin/python3
'''DB Storage engine script'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.base_model import Base
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.review import Review
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.place import place_amenity

classes = {"User": User, "State": State, "City": City,
           "Amenity": Amenity, "Place": Place, "Review": Review}


class DBStorage:
    '''storage for mysql'''
    __engine = None
    __session = None

    def __init__(self):
        '''instantiating storage'''
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_ENV = getenv('HBNB_ENV')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                                           HBNB_MYSQL_USER,
                                           HBNB_MYSQL_PWD,
                                           HBNB_MYSQL_HOST,
                                           HBNB_MYSQL_DB
                                       ), pool_pre_ping=True)

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''returns all class objects. If cls is not none,
        returns cls objects alone
        '''
        object_dict = {}
        if cls is None:
            for model_class in classes.values():
                query_result = self.__session.query(model_class).all()
                for single in query_result:
                    key = single.__class__.__name__ + '.' + single.id
                    object_dict[key] = single
        else:
            query_result = self.__session.query(cls).all()
            for single in query_result:
                key = single.__class__.__name__ + '.' + single.id
                object_dict[key] = single
        return object_dict

    def new(self, obj):
        '''Creates new object'''
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def save(self):
        '''commits changes'''
        self.__session.commit()

    def delete(self, obj=None):
        ''' removes data from db
        '''
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete()

    def reload(self):
        '''triggers database reload'''
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """quits the current working session"""
        self.__session.close()
