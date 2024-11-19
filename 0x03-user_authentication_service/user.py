#!/usr/bin/env python3
""" User Model """
import bcrypt
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """ User class for mapping user instances to database """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))

    def __init__(self, *args, **kwargs):
        """ Initializes a User instance """
        for key, value in kwargs.items():
            setattr(self, key, value)
