#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Information about this API.

.. currentmodule:: {{cookiecutter.package_name}}.apis.info
.. moduleauthor:: {{cookiecutter.author_name}} <{{cookiecutter.author_email}}>
"""
from flask_restx import Namespace, Resource, fields
from flask_restx.model import Model
from .. import __version__

api = Namespace('info', description='Get general information about the API.')

InfoModel: Model = api.model(
    'Info',
    {
        'version': fields.String(
            readOnly=True,
            description='the API version'
        )
    }
)  #: the information model


@api.route('/')
class InfoResource(Resource):
    """Get general information about the API."""
    @api.doc('get_info')
    @api.marshal_with(InfoModel, envelope='info')
    def get(self):  # pylint: disable=no-self-use
        """Get general information about the API."""
        return {
            'version': __version__
        }, 200
