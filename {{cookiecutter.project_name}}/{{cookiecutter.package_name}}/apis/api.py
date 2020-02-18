#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API descriptions.

.. currentmodule:: {{cookiecutter.package_name}}.apis.api
.. moduleauthor:: {{cookiecutter.author_name}} <{{cookiecutter.author_email}}>
"""
import json
import logging
from flask_restx import Api
from werkzeug.exceptions import HTTPException
from .. import __version__
from .crud import api as crud
from .info import api as info

API_ROOT: str = '/api'  #: the common root for API routes

LOGGER: logging.Logger = logging.getLogger(__name__)  #: the module logger

EX_CODES = {
    KeyError: 404
}  #: HTTP codes for exception types

# Create the API object.
api = Api(
    title='{{cookiecutter.project_name}}',
    version=__version__,
    description='{{cookiecutter.project_description}}'
    # Add other API metadata here.
)

# Add the namespaces.
api.add_namespace(crud, path='/crud')
api.add_namespace(info, path='/info')


@api.errorhandler(Exception)
def handle_ex(ex: Exception):
    """Last-resort exception handling."""

    # Log the fact that the default handler had to handle the exception.
    LOGGER.exception(ex)

    # If this is a werkzeug HTTP exception, we can provide certain kinds
    # of helpful information...
    if isinstance(ex, HTTPException):
        return json.dumps({
            'code': ex.code,
            'name': ex.name,
            'type': type(ex).__name__,
            'message': ex.description
        })
    # Otherwise, return some basic information.
    return {
        'type': type(ex).__name__,
        'message': str(ex),
    }, EX_CODES.get(type(ex), 500)
