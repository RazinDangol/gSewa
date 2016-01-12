from celery import Celery




app = Celery('task',broker='redis://localhost:6379/0')

@app.task
def sum(a,b):
    return a+b
