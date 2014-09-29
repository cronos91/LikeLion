"""
Initialize Flask app

"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.email import ConsoleMail

app = Flask('apps')
app.config.from_object('apps.settings.Production')

mailbox = ConsoleMail(app)
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

import controllers, models