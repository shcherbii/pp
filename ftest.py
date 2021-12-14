import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool
from main import *
import json
from models import *
from flask import Flask
#from flask_pytest_example.handlers.routes import configure_routes
from schemas import *

user_user = {
    "email": "user1@gmail.com",
    "firstName": "User1",
    "idUser": 2,
    "lastName": "UserLastname1",
    "login": "user1",
    "password": "1111",
    "phone": "0680708908",
    "user_status": "User"
}
user = User(firstName='Vladyslav', lastName='Diachyk', login='vld_dchk228', email='exampl@gmail.com',
            phone='+380957777777', password='12345678',user_status = 'User')

# user_admin = {"id":2, "name":"f", "surname":"s", "username":"Admin_A", "password":"1", "accessusers":"Admin"}
# wrong_user = {"id":3, "name":"f", "surname":"s", "username":"username3_A", "password":"1", }
# Abslut_wrong_user = { "id":3,"name":"f", "surname":"s", "username":"Admin_A","accessusers":"Admin" }
# user_without_id = {"name":"f", "surname":"s", "username":"username3", "password":"1","accessusers":"Admin" }
# wrong_user_without_id = {"name":"f", "username":"username3","accessusers":"Admin" }

session = Session()

@pytest.fixture(scope="session")
def client():
    session.query(Reservation).delete()
    session.query(Car).delete()
    session.query(User).delete()
    client = create_app().test_client()
    yield client
    session.query(Reservation).delete()
    session.query(Car).delete()
    session.query(User).delete()
    session.commit()

# @pytest.fixture()
# def user_C():
#     User_c = User(id=3, name="username1",  username = "User", surname="username1",
#                 password="1", accessusers="User")
#     session.add(User_c)
#     session.commit()
#     return User_c

@pytest.fixture()
def login_User(client):

    # client.post(BASE_PATH + USER_PATH, json=user_user)
    #response = client.post(BASE_PATH + 'user', data=json.dumps(user_user), content_type='application/json')
    session.add(user)
    session.commit()
    access_token = create_access_token(identity="vld_dchk228") # user_user.get('login')
    #res = client.post(BASE_PATH + USER_PATH+ '/login', json=user_user)
    res = {"token":access_token}
    return res

# @pytest.fixture()
# def login_Admin(client):
#     res = client.post('/register', json=user_admin)
#     return res.get_json()


# student1= {"id":1, "firstname":"f", "surname":"s", "course":4, "best_grade":4, "created":0}
# student2 = {"id":2, "firstname":"f", "surname":"s", "course":4, "best_grade":4, "created":0}
# wrong_student2 = {"id":2, "course":4, "best_grade":4, "created":0}
# student_without_id = { "firstname":"f", "surname":"s", "course":4, "best_grade":4, "created":0}
# wrong_student_without_id = { "firstname":"f", "surname":"s", "course":4, "best_grade":4, "created":0}
#
# @pytest.fixture()
# def Student_C(user_C):
#     Student_c = Student(id=3, firstname="f",
#                         surname = "s", course=4,
#                         created = user_C.id, best_grade=1)
#     session.add(Student_c)
#     session.commit()
#     return Student_c
#
# @pytest.fixture()
# def Student_C_login(login_User):
#     Student_c = Student(id=4, firstname="f",
#                         surname = "s", course=4,
#                         created = login_User['new_user_id'], best_grade=1)
#     session.add(Student_c)
#     session.commit()
#     return Student_c
#
#
# reting1 = {"id":3, "title":"f", "Student_id":0, "user_creator_id":0}
# reting_without = {"title":"f", "Student_id":0, "user_creator_id":0}
# @pytest.fixture()
# def Rating_C(Student_C , user_C):
#     Rating_c = Rating(title = 'f',Student_id = Student_C.id, user_creator_id =  user_C.id)
#     session.add(Rating_c)
#     session.commit()
#     return Rating_c
#
# @pytest.fixture()
# def Rating_C_login(login_Admin, Student_C):
#
#     Rating_c = Rating(id = 5, title = 'f',Student_id = Student_C.id, user_creator_id = login_Admin['new_user_id'])
#     session.add(Rating_c)
#     session.commit()
#     return Rating_c