from flask import Flask, render_template, request, redirect , url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug import secure_filename
import os
# Making celery instance 
from celery import Celery
def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

# configurations
app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)



from models import *
from task import *

info = db.session.query(Info).first()

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
            populate.delay(os.path.join(os.getcwd(),'upload',filename))
            return redirect(url_for('payment',service_provider='all'))
        else:
            flash('Please upload datasheet of excel format')
            return render_template('index.html')
    return render_template('index.html')


@app.route('/payment/<service_provider>')
def payment(service_provider):
    if service_provider.lower() == 'all':
        payments = db.session.query(Payment).all()
    else:
        payments = db.session.query(Payment).filter_by(
            service_provider=service_provider.upper())
    total = db.session.query(Payment.service_provider, func.count(
        Payment.amount), func.sum(Payment.amount)).group_by(Payment.service_provider)
    
    
    return render_template('payment.html', payments=payments, service_provider=service_provider, total=total,info=info)


@app.route('/cashback/<service_provider>')
def cashback(service_provider='all'):
    if service_provider.lower() == 'all' or service_provider is None:
        cashbacks = db.session.query(Cashback).all()
    else:
        cashbacks = db.session.query(Cashback).filter_by(
            service_provider=service_provider.upper())
    total = db.session.query(Cashback.service_provider, func.count(
        Cashback.amount), func.sum(Cashback.amount)).group_by(Cashback.service_provider)
    return render_template('cashback.html', cashbacks=cashbacks, service_provider=service_provider, total=total,info=info)


if __name__ == '__main__':
    app.run(debug=True)
