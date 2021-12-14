from main import *

from models import *
import json
import pytest
#from main import app
from main import create_app
from constants import *
from ftest import *
from flask.testing import FlaskClient
from sqlalchemy import create_engine

token1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmc' \
         'mVzaCI6ZmFsc2UsImlhdCI6MTYzOTM1NjgxNywianRpIjoi' \
         'YzQ5NjVhNzgtN2IxMi00ZGM3LTgxYmQtZmI0YWI2NGNjZGI5Iiwid' \
         'HlwZSI6ImFjY2VzcyIsInN1YiI6InVyYXN1ayIsIm5iZiI6MTYzOTM' \
         '1NjgxNywiZXhwIjoxNjM5MzU3NzE3fQ.Unaw4Trk1ys1Kd143pzX9GZ_dVOF6HXzJD7Z2cg6LzE'

# @pytest.fixture
# def app():
#     app = create_app()
#     return app

session = Session()

@pytest.fixture
def app():
    # engine = create_engine(DB_URL, echo=False)
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine, )
    app = create_app()
    app_context = app.app_context()
    return app

# @pytest.fixture(scope="session")
# def client():
#     session.query(Reservation).delete()
#     session.query(Car).delete()
#     session.query(User).delete()
#     client = create_app().test_client()
#     yield client
#     session.query(Reservation).delete()
#     session.query(Car).delete()
#     session.query(User).delete()
#     session.commit()


#app_context.push()
#client = app.test_client()

#
# def create_user(client, login, password):
#     response = client.post(USER_PATH, data=dict(
#         login=login,
#         password=password
#     ))
#     return response
#
# def login(client, username, password):
#     response = client.get('/user/login', data=dict(
#         username=username,
#         password=password
#     ))
#     return response
#
# def logout(client, token):
#     response = client.get('/user/logout', headers=[('Authorization', f'Bearer {token}')])
#     return response
#
#
# def user_id(client, user_id, token):
#     response = client.get(f'/user/{user_id}', headers=[('Authorization', f'Bearer {token}')])
#     return response




def test_create_user_successfully(client):
    #session = Session()
    send_data = {
        "email": "newUser5@gmail.com",
        "firstName": "NEW5",
        "idUser": 1,
        "lastName": "NEW5ррр",
        "login": "new5",
        "password": "1111",
        "phone": "0690717920",
        "user_status": "User"
    }
    response = client.post(BASE_PATH + 'user', data=json.dumps(send_data), content_type='application/json')
    # session.query(User).filter_by(login=send_data["login"]).delete()
    assert response.status_code == 201

def test_create_user_successfully2(client):
    #session = Session()
    send_data = {
        "email": "ksUser5@gmail.com",
        "firstName": "Ksenia",
        "idUser": 5,
        "lastName": "Teterina",
        "login": "ksena",
        "password": "1111",
        "phone": "0690710920",
        "user_status": "Admin"
    }
    response = client.post(BASE_PATH + 'user', data=json.dumps(send_data), content_type='application/json')
    # session.query(User).filter_by(login=send_data["login"]).delete()
    assert response.status_code == 201

def test_create_user_existing_login(client):
    send_data = {
        "email": "ks@gmail.com", # !
        "firstName": "Ksenia",
        "idUser": 6,
        "lastName": "Teterina",
        "login": "new5",
        "password": "1111",
        "phone": "0682708928",
        "user_status": "Admin"
    }
    response = client.post(BASE_PATH + 'user', data=json.dumps(send_data), content_type='application/json')
    assert response.status_code == 409

def test_create_user_existing_id(client):
    send_data = {
        "email": "ks@gmail.com",
        "firstName": "Ksenia",
        "idUser": 1, # !
        "lastName": "Teterina",
        "login": "ksena2",
        "password": "1111",
        "phone": "0682708928",
        "user_status": "Admin"
    }
    response = client.post(BASE_PATH + 'user', data=json.dumps(send_data), content_type='application/json')
    assert response.status_code == 409

def test_create_user_existing_prop(client):
    send_data = {
        "email": "newUser5@gmail.com", # !
        "firstName": "Oleg",
        "idUser": 9,
        "lastName": "Senja",
        "login": "some",
        "password": "1111",
        "phone": "0689908928",
        "user_status": "User"
    }
    response = client.post(BASE_PATH + 'user', data=json.dumps(send_data), content_type='application/json')
    assert response.status_code == 400

def test_create_user_existing_prop2(client):
    send_data = {
        "email": "ksgu@gmail.com",
        "firstName": "Oleg",
        "idUser": 9,
        "lastName": "Senja",
        "login": "some",
        "password": "1111",
        "phone": "0690717920", # !
        "user_status": "User"
    }
    response = client.post(BASE_PATH + 'user', data=json.dumps(send_data), content_type='application/json')
    assert response.status_code == 400


def test_get_user():
    try:
        user1 = session.query(User).filter_by(login="new5").first()
        access_token = create_access_token(identity='new5')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        url = BASE_PATH + 'user/' + str(user1.idUser)
        # str(user1.id)
        response = client.get(url, headers=headers)
        assert response.status_code == 200
        session.commit()
    except:
        session.rollback()

# ?
def test_get_all_users_success():
    try:
        user1 = session.query(User).filter_by(login="ksena").all()
        access_token = create_access_token(identity='ksena')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        url = BASE_PATH + 'user'
        # str(user1.id)
        response = client.get(url, headers=headers)
        assert response.status_code == 200


        session.commit()
    except:
        session.rollback()


# def test_get_user_by_id(client,login_User):
#     user_token = login_User['token']
#     #access_token = create_access_token(identity='new5')
#     headers = {'Authorization': 'Bearer ' + token1}
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer ' + user_token
#
#     }
#     response = client.get(BASE_PATH + 'user/' + f'{1}', headers=headers)
#
#     assert response.status_code == 200
#     # assert json.loads(response.data) == {
#     #     "email": "yura@gmail.com",
#     #     "firstName": "Yura",
#     #     "idUser": 3,
#     #     "lastName": "Yanio",
#     #     "login": "urasuk",
#     #     "password": "$2b$12$wNDStdfgeubsNKBJUeDOteWHFIwbYV1oJfsrXhLCcKccn9vIq8V4W",
#     #     "phone": "0682608928",
#     #     "user_status": "User"
#     # }


def test_delete_user():

    try:
        url = '/api/v1/user'

        user = session.query(User).filter_by(username="ksena").first()
        access_token = create_access_token(identity='ksena')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        url = '/api/v1/user'
        response = client.delete(url, headers=headers)
        session.commit()
        assert response.status_code == 200
    except:
        session.rollback()


#
# def test_create_event():
#     send_data = {
#         "username": "pipasd",
#         "firstName": "abdul",
#         "lastName": "hamid",
#         "password": "Basiloks",
#         "email": "iam@mail.ua",
#         "phone": "+380665066053"
#     }
#
#     url = '/api/v1/user'
#     response = client.post(url, data=json.dumps(send_data), content_type='application/json')
#     session.commit()
#     user = session.query(User).filter_by(username="pipasd").first()
#     access_token = create_access_token(identity=user.username)
#     headers = {
#         'Authorization': 'Bearer {}'.format(access_token)
#     }
#     send_data = {
#         'header': "something",
#         'description': "something",
#         'date': "2011-11-03 18:21:26"
#     }
#     url = '/api/v1/events'
#     response = client.post(url, data=json.dumps(send_data), content_type='application/json', headers=headers)
#     session.commit()
#     assert response.status_code == 200
#     url = '/api/v1/system'
#     response = client.get(url, headers=headers)
#     assert response.status_code == 200
#     send_data = {
#         'header': "somethin",
#         'description': "somethin",
#         'date': "2011-11-03 18:21:25"
#     }
#     temp = session.query(Events).order_by(Events.id.desc()).first()
#     url = '/api/v1/events/' + str(temp.id)
#     response = client.get(url, headers=headers)
#     assert response.status_code == 200
#     response = client.put(url, data=json.dumps(send_data), content_type='application/json', headers=headers)
#     session.commit()
#     assert response.status_code == 200
#     session.query(System).filter_by(userId=user.id).delete()
#     session.query(User).filter_by(id=user.id).delete()
#     session.query(Events).filter_by(header="somethin").delete()
#     session.commit()
#
#
# def test_get_events():
#     url = '/api/v1/events'
#     response = client.get(url)
#     assert response.status_code == 200
#
#
# def test_delete_events():
#     send_data = {
#         "username": "pipasd",
#         "firstName": "abdul",
#         "lastName": "hamid",
#         "password": "Basiloks",
#         "email": "iam@mail.ua",
#         "phone": "+380665066053"
#     }
#
#     url = '/api/v1/user'
#     response = client.post(url, data=json.dumps(send_data), content_type='application/json')
#     session.commit()
#     user = session.query(User).filter_by(username="pipasd").first()
#     access_token = create_access_token(identity=user.username)
#     headers = {
#         'Authorization': 'Bearer {}'.format(access_token)
#     }
#     send_data = {
#         'header': "some",
#         'description': "something",
#         'date': "2011-11-03 18:21:26"
#     }
#     url = '/api/v1/events'
#     response = client.post(url, data=json.dumps(send_data), content_type='application/json', headers=headers)
#     session.commit()
#     temp = session.query(Events).order_by(Events.id.desc()).first()
#     session.commit()
#     session.query(System).filter_by(userId=user.id).delete()
#     session.commit()
#     url = '/api/v1/events/' + str(temp.id)
#     response = client.delete(url, headers=headers)
#     session.query(User).filter_by(id=user.id).delete()
#     session.commit()
#     assert response.status_code == 200
#




