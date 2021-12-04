from models import Session, User, Car, StatusCar, Reservation, StatusReservation

session = Session()

user = User(firstName='Vladyslav', lastName='Diachyk', login='vld_dchk228', email='exampl@gmail.com',
            phone='+380957777777', password='12345678',user_status = 'User')

user1 = User(firstName='Admin_first', lastName='AdminAdminuch', login='admin1', email='udmin1@gmail.com',
            phone='+380957777788', password='1234567890',user_status = 'Admin')

status_car1 = StatusCar(name='available')
status_car2 = StatusCar(name='unavailable')

car1 = Car(name='BMW X5', productionYear=2019, price=300.50, minDays=3, maxDays=14, idStatusCar=1)
car2 = Car(name='Audi Q7', productionYear=2021, price=400, maxDays=7, idStatusCar=2)

status_reserv1 = StatusReservation(name='placed')
status_reserv2 = StatusReservation(name='confirmed')
status_reserv3 = StatusReservation(name='canceled')

reserv1 = Reservation(startDate='2021-10-25', endDate='2021-10-29', sum=1202, idUser=1, idCar=1, idStatusReserv=1)
reserv2 = Reservation(startDate='2021-10-27', endDate='2021-11-04', sum=3400, idUser=1, idCar=2, idStatusReserv=3)

session.add(user)
session.add(user1)

session.add(status_car1)
session.add(status_car2)

session.add(car1)
session.add(car2)

session.add(status_reserv1)
session.add(status_reserv2)
session.add(status_reserv3)

session.add(reserv1)
session.add(reserv2)

session.commit()

print(session.query(User).all()[0])
print(session.query(Car).all())
print(session.query(StatusCar).all())
print(session.query(Reservation).all())
print(session.query(StatusReservation).all())

session.close()
