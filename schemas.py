from models import User, Car, StatusCar, Reservation, StatusReservation
from marshmallow import Schema


class UserSchema(Schema):
    class Meta:
        model = User
        fields = ('idUser', 'firstName', 'lastName', 'login', 'email', 'phone', 'password', 'user_status')


class CarSchema(Schema):
    class Meta:
        model = Car
        fields = ('idCar', 'name', 'productionYear', 'price', 'minDays', 'maxDays', 'idStatusCar')


class StatusCarSchema(Schema):
    class Meta:
        model = StatusCar
        fields = ('idStatusCar', 'name')


class ReservationSchema(Schema):
    class Meta:
        model = Reservation
        fields = ('idReservation', 'startDate', 'endDate', 'sum', 'idUser', 'idCar', 'idStatusReserv')


class StatusReservationSchema(Schema):
    class Meta:
        model = StatusReservation
        fields = ('idStatusReserv', 'name')

