#!/usr/bin/env python3
""" DB module

Class:
    DB: Handles database operations
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class for database operations
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds a new user to the database

        Args:
            email (str): User email
            hashed_password (str): User's password (hashed)

        Returns:
            New user
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None

        return user

    def find_user_by(self, **kwargs) -> User:
        """ Finds a user in database

        Args:
            kwargs: attribute to search database with

        Returns:
            First match in users table

        Examples:
            >>> db = DB()
            >>> user = db.find_user_by(email="test@hbtn.io")
            >>> user1 = db.find_user_by(no_email="test2@hbtn.io")
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates a user

        Args:
            user_id (int): User int
            kwargs (dict): attributes to update with respective values

        Returns:
            None

        Examples:
            >>> db = DB()
            >>> db.update_user(1, hashed_password="HashedPassword1")
        """
        user = self.find_user_by(id=user_id)
        if not user:
            return

        for key, value in kwargs.items():
            try:
                getattr(user, key)
            except AttributeError:
                raise ValueError
            setattr(user, key, value)

        self._session.commit()
        return
