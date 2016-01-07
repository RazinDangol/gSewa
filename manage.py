from flask.ext.script import Manager, Command
import parse
from db_create import *
from gsewa import app

manager=Manager(app)

@manager.command
def init_db(doc_name):
    db.drop_all()
    db.create_all()
    info(doc_name)
    populate(doc_name)


if __name__=='__main__':
    manager.run()