from gsewa import db

class Payment(db.Model):
    __tablename__ = "payment"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    service_provider=db.Column(db.String)
    service = db.Column(db.Text)
    service_name = db.Column(db.String)
    service_type = db.Column(db.String)
    amount = db.Column(db.Integer)
    status = db.Column(db.String)
    time = db.Column(db.String)

    def __init__(self,service_provider,service,service_name,service_type,amount,status,time):
        self.service_provider = service_provider
        self.service = service
        self.service_name = service_name
        self.service_type = service_type
        self.amount = amount
        self.status = status
        self.time = time
    def __repr__(self):
        return '{}'.format(str(self.service_provider))

class Cashback(db.Model):
    __tablename__ = "cashback"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    service_provider=db.Column(db.String)
    service = db.Column(db.Text)
    service_name = db.Column(db.String)
    service_type = db.Column(db.String)
    amount = db.Column(db.Integer)
    status = db.Column(db.String)
    time = db.Column(db.String)
    def __init__(self,service_provider,service,service_name,service_type,amount,status,time):
        self.service_provider = service_provider
        self.service = service
        self.service_name = service_name
        self.service_type = service_type
        self.amount = amount
        self.status = status
        self.time = time
    def __repr__(self):
        return '{}'.format(self.service_provider)

class Transfer(db.Model):
    __tablename__ = "transfer"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    service_provider=db.Column(db.String)
    service = db.Column(db.Text)
    service_name = db.Column(db.String)
    service_type = db.Column(db.String)
    amount = db.Column(db.Integer)
    status = db.Column(db.String)
    time = db.Column(db.String)
    name = db.Column(db.String)
    def __init__(self,service_provider,service,service_name,service_type,amount,status,time,name):
        self.service_provider = service_provider
        self.service = service
        self.service_name = service_name
        self.service_type = service_type
        self.amount = amount
        self.status = status
        self.time = time
        self.name = name
    def __repr__(self):
        return '{}'.format(self.service_provider)

class Info(db.Model):
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    esewa_id = db.Column(db.String)

    def __init__(self,esewa_id):
        self.esewa_id = esewa_id

    def __repr__(self):
        return '{}'.format(self.esewa_id)

class Other(db.Model):
    __tablename__ = 'other'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    service_provider=db.Column(db.String)
    service = db.Column(db.Text)
    service_name = db.Column(db.String)
    service_type = db.Column(db.String)
    amount = db.Column(db.Integer)
    status = db.Column(db.String)
    time = db.Column(db.String)

    def __init__(self,service_provider,service,service_name,service_type,amount,status,time):
        self.service_provider = service_provider
        self.service = service
        self.service_name = service_name
        self.service_type = service_type
        self.amount = amount
        self.status = status
        self.time = time
    def __repr__(self):
        return '{}'.format(str(self.service_provider))