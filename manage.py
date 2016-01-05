from flask.ext.script import Manager, Command
import parse
import db
from gsewa import app

manager=Manager(app)



if __name__=='__main__':
    db.init_db()
    db.populate()
    manager.run()