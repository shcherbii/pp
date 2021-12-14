import sys

from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    ForeignKey,
    Date,
)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship

sys.path.append(r"D:\lab9_pp\pp")

DB_URL = "mysql+mysqlconnector://root:sqlLp9lp@localhost:3306/car_service"

engine = create_engine(DB_URL)

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = "user"

    idUser = Column(Integer, primary_key=True, unique=True)
    firstName = Column(String(length=45), nullable=False)
    lastName = Column(String(length=45), nullable=False)
    login = Column(String(length=45), nullable=False, unique=True)
    email = Column(String(length=45), nullable=False, unique=True)
    phone = Column(String(length=45), nullable=False, unique=True)
    password = Column(String(length=75), nullable=False)
    user_status = Column(String(length=75), nullable=False)
    reservations = relationship("Reservation", back_populates="user")

    def __str__(self):
        return f"user ID : {self.idUser}\n" \
               f"firstName : {self.firstName}\n" \
               f"lastName : {self.lastName}\n" \
               f"login : {self.login}\n" \
               f"email : {self.email}\n" \
               f"phone : {self.phone}\n" \
               f"password : {self.password}\n"


class Car(BaseModel):
    __tablename__ = "car"

    idCar = Column(Integer, primary_key=True, unique=True)
    name = Column(String(length=45), nullable=False)
    productionYear = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    minDays = Column(Integer)
    maxDays = Column(Integer)
    idStatusCar = Column(Integer, ForeignKey("status_car.idStatusCar"))

    status_car = relationship("StatusCar")
    reservations = relationship("Reservation", back_populates="car")

    def __str__(self):
        return f"Car ID : {self.idCar}\n" \
               f"Name : {self.name}\n" \
               f"Production year : {self.productionYear}\n" \
               f"Price : {self.price}\n" \
               f"minDays : {self.minDays}\n" \
               f"maxDays : {self.maxDays}\n" \
               f"idStatusCar : {self.idStatusCar}\n"


class StatusCar(BaseModel):
    __tablename__ = "status_car"

    idStatusCar = Column(Integer, primary_key=True, unique=True)
    name = Column(String(length=45), nullable=False)


class Reservation(BaseModel):
    __tablename__ = "reservation"
    idReservation = Column(Integer, primary_key=True, unique=True)
    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)
    sum = Column(DECIMAL(10, 2), nullable=False)
    idUser = Column(Integer, ForeignKey("user.idUser"))
    idCar = Column(Integer, ForeignKey("car.idCar"))
    idStatusReserv = Column(Integer, ForeignKey("status_reservation.idStatusReserv"))

    user = relationship("User", back_populates="reservations")
    car = relationship("Car", back_populates="reservations")
    status_reservation = relationship("StatusReservation", back_populates="reservations")


class StatusReservation(BaseModel):
    __tablename__ = "status_reservation"

    idStatusReserv = Column(Integer, primary_key=True, unique=True)
    name = Column(String(length=45), nullable=False)

    reservations = relationship("Reservation", back_populates="status_reservation")

# class CarImage(BaseModel):
#     __tablename__ = "car_image"
#
#     idCar = Column(Integer, ForeignKey("car.idCar"))
#     file = Column(String(length=100), nullable=False)
#
#     car = relationship("Car")
# alembic revision --autogenerate -m "First"
# alembic upgrade head
