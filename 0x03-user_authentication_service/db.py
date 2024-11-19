"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User
from typing import TypeVar


class DB:
    """DB class
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
            DBSession = sessionmaker(bind=self._engine, echo=True)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """ Saves a user to the database

        Args:
            email (str): User email
            hashed_password (str): User's password (hashed)

        Returns:
            User object.
        """
        if not email or not isinstance(email, str):
            return None
        if not hashed_password or not isinstance(hashed_password, str):
            return None

        data = {'email': email, 'hashed_password': hashed_password}
        session = self._session

        user = User(**data)
        session.add(user)
        session.commit()
        return user
