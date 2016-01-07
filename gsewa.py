from flask import Flask, render_template, request, redirect , url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug import secure_filename
import os
from db_create import *
from rq import Queue
from rq.job import Job
from worker import conn
 

# configurations
app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
q = Queue(connection = conn)
from models import *


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            
            
            job = q.enqueue_call(func = populate, 
            args=('esewa.xls',))
            
            return 'success'
    return render_template('index.html')


@app.route('/payment/<service_provider>')
def payment(service_provider='all'):
    if service_provider.lower() == 'all' or service_provider is None:
        payments = db.session.query(Payment).all()
    else:
        payments = db.session.query(Payment).filter_by(
            service_provider=service_provider.upper())
    total = db.session.query(Payment.service_provider, func.count(
        Payment.amount), func.sum(Payment.amount)).group_by(Payment.service_provider)
    return render_template('payment.html', payments=payments, service_provider=service_provider, total=total)


@app.route('/cashback/<service_provider>')
def cashback(service_provider='all'):
    if service_provider.lower() == 'all' or service_provider is None:
        cashbacks = db.session.query(Cashback).all()
    else:
        cashbacks = db.session.query(Cashback).filter_by(
            service_provider=service_provider.upper())
    total = db.session.query(Cashback.service_provider, func.count(
        Cashback.amount), func.sum(Cashback.amount)).group_by(Cashback.service_provider)
    return render_template('cashback.html', cashbacks=cashbacks, service_provider=service_provider, total=total)


if __name__ == '__main__':
    app.run(debug=True)
