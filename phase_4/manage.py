from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from schedules import app, db

migrate = Migrate(app.flask_app, db)
manager = Manager(app.flask_app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
	from models.record import Record
	manager.run()