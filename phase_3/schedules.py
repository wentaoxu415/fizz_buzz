from application import Application, handlers
import os

app = Application(handlers, os.environ, debug=False)
celery = app.celery()

import tasks

