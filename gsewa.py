from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, make_response
from werkzeug import secure_filename
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os


# Making celery instance
from celery import Celery
import dataset
app = Flask(__name__)
app.config.from_pyfile('config.py')


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


 
# Making SqlAlchemy instance of the app
db = SQLAlchemy(app)
from models import *
from task import *


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/payment/<service_provider>')
def payment(service_provider):
    info = db.session.query(Info).first()
    service_providers = db.session.query(
        Payment.service_provider).group_by(Payment.service_provider)
    if service_provider.lower() == 'all':
        payments = db.session.query(Payment).all()
        complete = db.session.query(Payment.service_provider, func.count(
            Payment.amount), func.sum(Payment.amount)).filter(Payment.status == "COMPLETE").group_by(Payment.service_provider)
        cancel = db.session.query(Payment.service_provider, func.count(
            Payment.amount), func.sum(Payment.amount)).filter(Payment.status == "CANCELED").group_by(Payment.service_provider)
    else:
        payments = db.session.query(Payment).filter_by(
            service_provider=service_provider.upper())
        complete = db.session.query(Payment.service_name, func.count(
            Payment.amount), func.sum(Payment.amount)).filter(Payment.status == "COMPLETE").filter_by(service_provider=service_provider.upper()).group_by(Payment.service_name)
        cancel = db.session.query(Payment.service_name, func.count(
            Payment.amount), func.sum(Payment.amount)).filter(Payment.status == "CANCELED").filter_by(service_provider=service_provider.upper()).group_by(Payment.service_name)

    return render_template('payment.html', payments=payments, service_providers=service_providers, complete=complete, cancel=cancel, info=info)


@app.route('/cashback/<service_provider>')
def cashback(service_provider='all'):
    info = db.session.query(Info).first()
    service_providers = db.session.query(
        Cashback.service_provider).group_by(Cashback.service_provider)
    if service_provider.lower() == 'all' or service_provider is None:
        cashbacks = db.session.query(Cashback).all()
        total = db.session.query(Cashback.service_provider, func.count(
            Cashback.amount), func.sum(Cashback.amount)).group_by(Cashback.service_provider)
    else:
        cashbacks = db.session.query(Cashback).filter_by(
            service_provider=service_provider.upper())
        total = db.session.query(Cashback.service_name, func.count(
            Cashback.amount), func.sum(Cashback.amount)).filter_by(service_provider=service_provider.upper()).group_by(Cashback.service_name)
    return render_template('cashback.html', cashbacks=cashbacks, total=total, info=info, service_providers=service_providers)


@app.route('/transfer/<service_provider>')
def transfer(service_provider='all'):
    if service_provider.lower() == 'all' or service_provider is None:
        transfers = db.session.query(Transfer).all()
    else:
        transfers = db.session.query(Transfer).filter_by(
            service_provider=service_provider.upper())
    received = db.session.query(Transfer.name, func.count(
        Transfer.amount), func.sum(Transfer.amount)).filter_by(service_name='received').group_by(Transfer.name)
    transferred = db.session.query(Transfer.name, func.count(
        Transfer.amount), func.sum(Transfer.amount)).filter_by(
        service_name='transferred').group_by(Transfer.name)
    info = db.session.query(Info).first()
    return render_template('transfer.html', transfers=transfers, service_provider=service_provider, received=received, transferred=transferred, info=info)


@app.route('/other', methods=['GET'])
def other():
    info = db.session.query(Info).first()
    others = db.session.query(Other).all()
    return render_template('others.html', others=others, info=info)


@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filedir = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filedir)
            task = populate.apply_async(args=[filedir])
            return jsonify({'location': url_for('taskstatus', task_id=task.id)})
        else:
            flash('Please upload datasheet of excel format')
            return redirect(url_for('index'))


@app.route('/status/<task_id>')
def taskstatus(task_id):
    print(task_id)
    task = populate.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {
            'state': 'PENDING',
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
        }
        if 'result' in str(task.info):
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
        }
    return jsonify(response)


@app.route('/job/<job_type>', methods=['GET'])
def missing_job(job_type):
    if job_type.lower() == 'missing':
        missing_job = missing_task.apply_async()

    else:
        export = export_job.delay()
    return 'Analysing data.....'


@app.route('/missing/<service_provider>')
def missing(service_provider):

    info = db.session.query(Info).first()
    service_providers = db.session.query(
        Cashback.service_provider).group_by(Cashback.service_provider)
    if service_provider.lower() == 'all' or service_provider is None:
        missings = db.session.query(Missing).all()
        total = db.session.query(Missing.service_provider, func.count(
            Missing.amount), func.sum(Missing.amount)).group_by(Missing.service_provider)
    else:
        missings = db.session.query(Missing).filter_by(
            service_provider=service_provider.upper())
        total = db.session.query(Missing.service_name, func.count(
            Missing.amount), func.sum(Missing.amount)).filter_by(service_provider=service_provider.upper()).group_by(Missing.service_name)
    return render_template('missing.html', missings=missings, total=total, info=info, service_providers=service_providers)


@app.route('/export', methods=['GET'])
def export():
    info = db.session.query(Info).first()
    filename = 'missing-{} - {}.txt'.format(
        str(info.from_date).replace('/', '-'), str(info.to_date).replace('/', '-'))
    f = open('missing/'+filename, 'r')
    response_data = f.read()
    response = make_response(response_data)
    response.headers['Content-Length'] = len(response_data)
    response.headers['Content-Type'] = 'text/txt'
    response.headers['Content-Disposition'] = 'attachment; filename=%s' % (
        filename)
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'public'
    return response


if __name__ == '__main__':
    app.run()
