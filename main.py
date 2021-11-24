import decimal
from datetime import datetime
from flask import Flask, request, jsonify
from constants import *
from schemas import *
from utils import *
import bcrypt
from flask.json import JSONEncoder


app = Flask(__name__)


class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return JSONEncoder.default(self, obj)


@app.route("/api/v1/hello-world-14")
def hello_world():
    return "<p>Hello World 14</p>"


# All about user
@app.route(BASE_PATH + USER_PATH, methods=['POST'])
def create_user():
    session = Session()
    try:
        user_request = request.get_json()

        user = User(**user_request)

        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password

        session.add(user)
        session.commit()

        return jsonify(USER_CREATED), 201
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + USER_PATH + '/' + '<int:idUser>', methods=['GET'])
def get_user_by_id(idUser):
    session = Session()
    try:
        user = session.query(User).filter_by(idUser=idUser).one()
    except:
        return jsonify(USER_NOT_FOUND), 404

    return jsonify(UserSchema().dump(user)), 200


@app.route(BASE_PATH + USER_PATH, methods=['GET'])
def get_all_users():
    session = Session()
    try:
        users = session.query(User).all()
    except:
        users = []

    users_dto = UserSchema(many=True)

    return jsonify(users_dto.dump(users)), 200


@app.route(BASE_PATH + USER_PATH + '/' + '<int:idUser>', methods=['PUT'])
def update_user(idUser):
    session = Session()
    try:
        if request.json['idUser']:
            return jsonify(CANT_CHANGE_ID), 400
    except:
        pass
    try:
        update_request = request.get_json()

        try:
            user = session.query(User).filter_by(idUser=idUser).one()
        except:
            return jsonify(USER_NOT_FOUND), 404

        update_user = update_util(user, update_request)

        if update_user is None:
            return jsonify(SOMETHING_WENT_WRONG), 400
        session.commit()
        return jsonify(USER_UPDATED), 200
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + USER_PATH + '/' + '<int:idUser>', methods=['DELETE'])
def delete_user(idUser):
    session = Session()
    try:
        user = session.query(User).filter_by(idUser=idUser).one()
    except:
        return jsonify(USER_NOT_FOUND), 404

    session.delete(user)
    session.commit()

    return jsonify(USER_DELETED), 200


# All about car
@app.route(BASE_PATH + CAR_PATH, methods=['POST'])
def place_car():
    session = Session()
    try:
        car_request = request.get_json()

        car = Car(**car_request)

        session.add(car)
        session.commit()

        return jsonify(CAR_PLACED), 201
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + CAR_PATH + '/' + '<int:idCar>', methods=['GET'])
def get_car_by_id(idCar):
    session = Session()
    try:
        car = session.query(Car).filter_by(idCar=idCar).one()
    except:
        return jsonify(CAR_NOT_FOUND), 404

    app.json_encoder = JsonEncoder
    return jsonify(CarSchema().dump(car)), 200


@app.route(BASE_PATH + CAR_PATH + '/' + '<int:idCar>', methods=['PUT'])
def edit_car(idCar):
    session = Session()
    try:
        if request.json['idCar']:
            return jsonify(CANT_CHANGE_ID), 400
    except:
        pass
    try:
        update_request = request.get_json()

        try:
            car = session.query(Car).filter_by(idCar=idCar).one()
        except:
            return jsonify(CAR_NOT_FOUND), 404

        update_car = update_util(car, update_request)

        if update_car is None:
            return jsonify(SOMETHING_WENT_WRONG), 400

        session.commit()
        return jsonify(CAR_EDITED), 200
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + CAR_PATH + '/' + '<int:idCar>', methods=['DELETE'])
def delete_car(idCar):
    session = Session()
    try:
        car = session.query(Car).filter_by(idCar=idCar).one()
    except:
        return jsonify(CAR_NOT_FOUND), 404
    session.delete(car)
    session.commit()

    return jsonify(CAR_DELETED), 200


# @app.route(BASE_PATH + CAR_PATH + '/' + '<int:idCar>' + CAR_IMAGE, methods=['POST'])
# def place_car():
#     session = Session()
#     try:
#         car_request = request.get_json()
#
#         car = CarImage(**car_request)
#
#         session.add(car)
#         session.commit()
#
#         return jsonify(IMAGE_PLACED), 201
#     except:
#         return jsonify(CAR_NOT_FOUND), 404


# All about reservation
@app.route(BASE_PATH + RESERVATION_PATH, methods=['POST'])
def create_reservation():
    session = Session()
    try:
        reservation_request = request.get_json()

        if session.query(Car.idCar).filter_by(idCar=reservation_request["idCar"]).scalar() is None:
            return jsonify(CAR_NOT_FOUND), 404

        if session.query(User.idUser).filter_by(idUser=reservation_request["idUser"]).scalar() is None:
            return jsonify(USER_NOT_FOUND), 404

        reservation = Reservation(**reservation_request)

        if datetime.strptime(str(reservation.startDate), '%Y-%m-%d') >= \
                datetime.strptime(str(reservation.endDate), '%Y-%m-%d'):
            return jsonify(INVALID_DATA), 400

        dfrom = datetime.strptime(str(reservation.startDate), '%Y-%m-%d')
        dto = datetime.strptime(str(reservation.endDate), '%Y-%m-%d')

        all_booked = session.query(Reservation).filter_by(idCar=reservation.idCar)
        for r in all_booked:
            if r.startDate <= dfrom.date() <= r.endDate:
                return jsonify(TIME_ALREADY_RESERVED), 400
            if r.startDate <= dto.date() <= r.endDate:
                return jsonify(TIME_ALREADY_RESERVED), 400
            if dfrom.date() <= r.startDate and dto.date() >= r.endDate:
                return jsonify(TIME_ALREADY_RESERVED), 400

        session.add(reservation)
        session.commit()

        return jsonify(RESERVATION_CREATED), 201
    except User.InvalidData:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + RESERVATION_PATH + '/' + '<int:idReservation>', methods=['GET'])
def get_reservation_by_id(idReservation):
    session = Session()
    try:
        reservation = session.query(Reservation).filter_by(idReservation=idReservation).one()
    except:
        return jsonify(RESERVATION_NOT_FOUND), 404

    app.json_encoder = JsonEncoder
    return jsonify(ReservationSchema().dump(reservation)), 200


@app.route(BASE_PATH + RESERVATION_PATH + '/' + '<int:idReservation>', methods=['PUT'])
def edit_reservation(idReservation):
    session = Session()
    try:
        if request.json['idReservation']:
            return jsonify(CANT_CHANGE_ID), 400

    except:
        pass
    try:
        update_request = request.get_json()

        try:
            playlist = session.query(Reservation).filter_by(idReservation=idReservation).one()
        except:
            return jsonify(RESERVATION_NOT_FOUND), 404

        if session.query(Car.idCar).filter_by(idCar=update_request["idCar"]).scalar() is None:
            return jsonify(CAR_NOT_FOUND), 404

        if session.query(User.idUser).filter_by(idUser=update_request["idUser"]).scalar() is None:
            return jsonify(USER_NOT_FOUND), 404

        update_reservation = update_util(playlist, update_request)

        if update_reservation is None:
            return jsonify(SOMETHING_WENT_WRONG), 400

        session.commit()
        return jsonify(RESERVATION_UPDATED), 200
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + RESERVATION_PATH + '/' + '<int:idReservation>', methods=['DELETE'])
def delete_reservation(idReservation):
    session = Session()
    try:
        reservation = session.query(Reservation).filter_by(idReservation=idReservation).one()
    except:
        return jsonify(RESERVATION_NOT_FOUND), 404
    session.delete(reservation)
    session.commit()

    return jsonify(RESERVATION_DELETED), 200


@app.route(BASE_PATH + RESERVATION_PATH + '/catalog', methods=['GET'])
def get_all_cars():
    session = Session()
    try:
        cars = session.query(Car).all()
    except:
        cars = []

    car_dto = CarSchema(many=True)

    app.json_encoder = JsonEncoder
    return jsonify(car_dto.dump(cars)), 200


@app.route(BASE_PATH + RESERVATION_PATH, methods=['GET'])
def get_all_reservations():
    session = Session()
    try:
        reservations = session.query(Reservation).all()
    except:
        reservations = []

    reservation_dto = ReservationSchema(many=True)

    app.json_encoder = JsonEncoder
    return jsonify(reservation_dto.dump(reservations)), 200


if __name__ == '__main__':
    app.run()

# waitress-serve --host 127.0.0.1 --port=5000 --call "main:create_app"
# http://127.0.0.1:5000/api/v1/hello-world-14
# venv\Scripts\activate
# curl -v -XGET http://localhost:5000/api/v1/hello-world-14
