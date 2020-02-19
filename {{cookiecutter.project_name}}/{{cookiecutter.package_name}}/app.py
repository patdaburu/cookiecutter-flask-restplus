#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Flask application.

.. currentmodule:: {{cookiecutter.package_name}}.app
.. moduleauthor:: {{cookiecutter.author_name}} <{{cookiecutter.author_email}}>
"""
import importlib
import logging
import os
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists
from . import config
from .apis import api, API_ROOT

# Determine which configuration set we're using.
_config = config.get_object_name()

# Create the Flask application.
app = Flask(__name__, static_url_path='')  #: the core Flask application
app.config.from_object(_config)

# Start up SQLAlchemy.
db = SQLAlchemy(app)
# Import the models.
importlib.import_module(
    '{{cookiecutter.package_name}}.models'
)

# Create this module's logger.
_logger: logging.Logger = logging.getLogger(__name__)  #: the module logger


# Log the configuration the app is using.
_logger.info(
    f"The application (PID={os.getpid()}) is initializing using the "
    f"'{config.get_name()}' configuration ({_config})."
)

# Continue Flask startup...
blueprint = Blueprint('api', __name__, url_prefix=API_ROOT)
api.init_app(blueprint)
app.register_blueprint(blueprint)
CORS(app)

# Set up special handling for static files.
if 'STATIC_FOLDER' in os.environ:
    app.static_folder = os.environ.get('STATIC_FOLDER')


@app.route('/')
def root():
    """Serve the default file."""
    return app.send_static_file('index.html')


def initdb():
    """Initialize the database (if it hasn't already been initialized)."""
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        db.create_all()
