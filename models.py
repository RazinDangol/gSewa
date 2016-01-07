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

    def __init__(self,service_provider,service,service_name,service_type,amount,status):
        self.service_provider = service_provider
        self.service = service
        self.service_name = service_name
        self.service_type = service_type
        self.amount = amount
        self.status = status

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
    
    def __init__(self,service_provider,service,service_name,service_type,amount,status):
        self.service_provider = service_provider
        self.service = service
        self.service_name = service_name
        self.service_type = service_type
        self.amount = amount
        self.status = status

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