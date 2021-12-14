import decimal
from datetime import datetime
from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_bcrypt import check_password_hash
from constants import *
from schemas import *
from utils import *
import jwt
import bcrypt
from flask.json import JSONEncoder
# from flask_pytest_example.handlers.routes import configure_routes


def create_app():
    app = Flask(__name__)

    app.config['TESTING'] = True

    app.config["JWT_SECRET_KEY"] = "super-secret"
    jwt = JWTManager(app)

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

            # з таким login
            try:
                if session.query(User).filter_by(login=user_request.get('login')).one():
                    return jsonify('User with this login already exists!'), 409
            except:
                pass

            # з таким userId
            try:
                if session.query(User).filter_by(idUser=user_request.get('idUser')).one():
                    return jsonify(USER_ALREADY_EXISTS), 409
            except:
                pass

            user = User(**user_request)

            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
            user.password = hashed_password

            session.add(user)
            session.commit()

            return jsonify(USER_CREATED), 201
        except:
            return jsonify(SOMETHING_WENT_WRONG), 400


    @app.route(BASE_PATH + USER_PATH + '/login', methods=['POST'])
    def login():
        # creates dictionary of form data
        auth = request.form

        if not auth or not auth.get('login') or not auth.get('password'):
            # returns 401 if any email or / and password is missing
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
            )
        session = Session()
        try:
            user = session.query(User).filter_by(login=auth.get('login')).one()
        except:
            return jsonify(USER_NOT_FOUND), 404

        if not user:
            # returns 401 if user does not exist
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
            )
        if check_password_hash(user.password, auth.get('password')):
            access_token = create_access_token(identity=user.login)
            return access_token

        # returns 403 if password is wrong
        return make_response(
            'Wrong password',
            403,
            {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
        )


    @app.route(BASE_PATH + USER_PATH + '/' + '<idUser>', methods=['GET'])
    @jwt_required()
    def get_user_by_id(idUser):
        try:
            idUser = int(idUser)
        except ValueError:
            return jsonify({"description": "Invalid parameters"}), 400

        current_identity_login = get_jwt_identity()

        session = Session()
        try:
            user = session.query(User).filter_by(idUser=idUser).one()
        except:
            return jsonify(USER_NOT_FOUND), 404
        user2 = session.query(User).filter_by(login=current_identity_login).one()
        if current_identity_login == user.login or user2.user_status == 'Admin':
            return jsonify(UserSchema().dump(user)), 200

        return jsonify('Access is denied'), 403




    @app.route(BASE_PATH + USER_PATH, methods=['GET'])
    @jwt_required()
    def get_all_users():
        current_identity_login = get_jwt_identity()

        session = Session()
        users = session.query(User).all()
        users_dto = UserSchema(many=True)
        user2 = session.query(User).filter_by(login=current_identity_login).one()
        if user2.user_status == 'Admin':
            return jsonify(users_dto.dump(users)), 200

        return jsonify('Access is denied'), 403


    @app.route(BASE_PATH + USER_PATH + '/' + '<int:idUser>', methods=['PUT'])
    @jwt_required()
    def update_user(idUser):
        current_identity_login = get_jwt_identity()
        session = Session()
        try:
            user = session.query(User).filter_by(idUser=idUser).one()
        except:
            return jsonify(USER_NOT_FOUND), 404
        if current_identity_login == user.login:
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

        return jsonify('Access is denied'), 403


    @app.route(BASE_PATH + USER_PATH + '/' + '<int:idUser>', methods=['DELETE'])
    @jwt_required()
    def delete_user(idUser):
        current_identity_login = get_jwt_identity()

        session = Session()
        try:
            user = session.query(User).filter_by(idUser=idUser).one()
        except:
            return jsonify(USER_NOT_FOUND), 404
        user2 = session.query(User).filter_by(login=current_identity_login).one()
        if current_identity_login == user.login or (user2.user_status == 'Admin' and user.user_status != 'Admin'):
            session.delete(user)
            session.commit()
            return jsonify(USER_DELETED), 200
        else:
            return jsonify('Access is denied'), 403


    # All about car
    @app.route(BASE_PATH + CAR_PATH, methods=['POST'])
    @jwt_required()
    def place_car():
        current_identity_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_identity_login).one()
        if user.user_status == 'Admin':
            try:
                car_request = request.get_json()

                car = Car(**car_request)

                session.add(car)
                session.commit()

                return jsonify(CAR_PLACED), 201
            except:
                return jsonify(SOMETHING_WENT_WRONG), 400
        else:
            return jsonify('Access is denied'), 403


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
    @jwt_required()
    def edit_car(idCar):
        current_identity_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_identity_login).one()
        if user.user_status == 'Admin':
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
        else:
            return jsonify('Access is denied'), 403


    @app.route(BASE_PATH + CAR_PATH + '/' + '<int:idCar>', methods=['DELETE'])
    @jwt_required()
    def delete_car(idCar):
        current_identity_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_identity_login).one()

        if user.user_status == 'Admin':
            try:
                car = session.query(Car).filter_by(idCar=idCar).one()
            except:
                return jsonify(CAR_NOT_FOUND), 404
            session.delete(car)
            session.commit()

            return jsonify(CAR_DELETED), 200
        else:
            return jsonify('Access is denied'), 403




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
    @jwt_required()
    def create_reservation():
        current_identity_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_identity_login).one()
        reservation_request = request.get_json()
        if user.user_status == 'User' and reservation_request["idUser"] == user.idUser:
            try:
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
            except:
                return jsonify(SOMETHING_WENT_WRONG), 400
        else:
            return jsonify('Access is denied'), 403


    @app.route(BASE_PATH + RESERVATION_PATH + '/' + '<int:idReservation>', methods=['GET'])
    @jwt_required()
    def get_reservation_by_id(idReservation):
        current_identity_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_identity_login).one()

        try:
            reservation = session.query(Reservation).filter_by(idReservation=idReservation).one()
        except:
            return jsonify(RESERVATION_NOT_FOUND), 404
        if (user.user_status == 'User' and reservation.idUser == user.idUser) or user.user_status == 'Admin':
            app.json_encoder = JsonEncoder
            return jsonify(ReservationSchema().dump(reservation)), 200
        else:
            return jsonify('Access is denied'), 403


    @app.route(BASE_PATH + RESERVATION_PATH + '/' + '<int:idReservation>', methods=['PUT'])
    @jwt_required()
    def edit_reservation(idReservation):
        current_identity_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_identity_login).one()
        try:
            rezerv = session.query(Reservation).filter_by(idReservation=idReservation).one()
        except:
            return jsonify(RESERVATION_NOT_FOUND), 404

        if user.user_status == 'User' and rezerv.idUser == user.idUser:
            try:
                if request.json['idReservation']:
                    return jsonify(CANT_CHANGE_ID), 400
            except:
                pass


            try:
                if request.json['idUser']:
                    return jsonify(CANT_CHANGE_ID), 400
            except:
                pass


            try:
                update_request = request.get_json()

                try:
                    rezervation = session.query(Reservation).filter_by(idReservation=idReservation).one()
                except:
                    return jsonify(CAR_NOT_FOUND), 404

                update_rezervation = update_util(rezervation, update_request)

                if update_rezervation is None:
                    return jsonify(SOMETHING_WENT_WRONG), 400

                session.commit()
                return jsonify(CAR_EDITED), 200
            except:
                return jsonify(SOMETHING_WENT_WRONG), 400
        else:
            return jsonify('Access is denied'), 403



    @app.route(BASE_PATH + RESERVATION_PATH + '/' + '<int:idReservation>', methods=['DELETE'])
    @jwt_required()
    def delete_reservation(idReservation):
        current_identity_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_identity_login).one()
        try:
            reservation = session.query(Reservation).filter_by(idReservation=idReservation).one()
        except:
            return jsonify(RESERVATION_NOT_FOUND), 404

        if (user.user_status == 'User' and reservation.idUser == user.idUser) or user.user_status == 'Admin':
            session.delete(reservation)
            session.commit()
            return jsonify(RESERVATION_DELETED), 200
        else:
            return jsonify('Access is denied'), 403


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
    @jwt_required()
    def get_all_reservations():
        current_identity_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_identity_login).one()
        if user.user_status == 'Admin':
            try:
                reservations = session.query(Reservation).all()
            except:
                reservations = []

            reservation_dto = ReservationSchema(many=True)

            app.json_encoder = JsonEncoder
            return jsonify(reservation_dto.dump(reservations)), 200
        else:
            return jsonify('Access is denied'), 403

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
    #app.run()

    # waitress-serve --host 127.0.0.1 --port=5000 --call "main:create_app"
    # http://127.0.0.1:5000/api/v1/hello-world-14
    # venv\Scripts\activate
    # curl -v -XGET http://localhost:5000/api/v1/hello-world-14
