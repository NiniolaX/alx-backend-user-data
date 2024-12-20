#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


my_db = DB()

user = my_db.add_user("test@test.com", "PwdHashed")
print(user.id)
user1 = my_db.add_user("test1@test.com", "PwdHashed1")
print(user.id)

find_user = my_db.find_user_by(email="test@test.com")
print(find_user.id)

find_user_1 = my_db.find_user_by(email="test1@test.com", hashed_password="PwdHashed1")
print(find_user_1.id)

try:
    find_user = my_db.find_user_by(email="test2@test.com")
    print(find_user.id)
except NoResultFound:
    print("Not found")

try:
    find_user = my_db.find_user_by(email=None)
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")
