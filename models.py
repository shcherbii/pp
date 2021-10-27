import os
import sys

from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    ForeignKey,
    Date,
)

from sqlalchemy import orm, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship

sys.path.append(r"C:\GitHub\ap_ostap")

DB_URL = "mysql+mysqlconnector://root:root@localhost/car_service"

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
    password = Column(String(length=45), nullable=False)

    def __str__(self):
        return f"User ID : {self.idUser}\n" \
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
    idStatusResev = Column(Integer, ForeignKey("status_reservation.idStatusResev"))

    user = relationship("User")
    car = relationship("Car")
    status_reservation = relationship("StatusReservation")


class StatusReservation(BaseModel):
    __tablename__ = "status_reservation"

    idStatusResev = Column(Integer, primary_key=True, unique=True)
    name = Column(String(length=45), nullable=False)

# alembic revision --autogenerate -m "First"
# alembic upgrade head
