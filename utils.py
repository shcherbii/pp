from models import Session


def find_by_id(model, id):
    session = Session()
    try:
        t = session.query(model).filter_by(id=id).one()
    except:
        return None
    return t


def update_util(model, data):
    try:
        if data.get('login', None):
            model.login = data['login']
        if data.get('password', None):
            model.password = data['password']
        if data.get('firstName', None):
            model.firstName = data['firstName']
        if data.get('lastName', None):
            model.lastName = data['lastName']
        if data.get('email', None):
            model.email = data['email']
        if data.get('phone', None):
            model.phone = data['phone']
        if data.get('name', None):
            model.name = data['name']
        if data.get('productionYear', None):
            model.productionYear = data['productionYear']
        if data.get('price', None):
            model.price = data['price']
        if data.get('minDays', None):
            model.minDays = data['minDays']
        if data.get('maxDays', None):
            model.maxDays = data['maxDays']
        if data.get('idStatusCar', None):
            model.idStatusCar = data['idStatusCar']
        if data.get('startDate', None):
            model.startDate = data['startDate']
        if data.get('endDate', None):
            model.endDate = data['endDate']
        if data.get('idStatusReserv', None):
            model.idStatusReserv = data['idStatusReserv']
        if data.get('sum', None):
            model.sum = data['sum']
    except:
        return None

    return model
