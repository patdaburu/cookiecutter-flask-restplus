#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple CRUD operations for demonstration purposes.

.. currentmodule:: {{cookiecutter.package_name}}.apis.info
.. moduleauthor:: {{cookiecutter.author_name}} <{{cookiecutter.author_email}}>
"""
from flask_restplus import Namespace, reqparse, Resource, fields
from flask_restplus.model import Model
from .. import __version__

api = Namespace('crud', description='Simple CRUD operations.')

ThingModel: Model = api.model(
    'Thing',
    {
        'name': fields.String(
            readOnly=False,
            description='the name of the Thing'
        )
    }
)  #: the Thing model

ThingRequestParser = reqparse.RequestParser()
thing.add_argument(
    'name',
    type=str,
    required=True
)  #: defines the parameters when you request a thing

THINGS = {
        'red': {'name': 'red'},
        'blue': {'name': 'blue'}
}  #: FOR DEMONSTRATION: a set of Things

@api.route('/')
class ThingResource(Resource):
    """Perform general CRUD operations."""
    @api.doc(params={})
    @api.marshal_with(ThingModel, envelope='things')
    def get(self):  # pylint: disable=no-self-use
        """Get the things."""
        return [
            v for k, v in THINGS.items()
        ], 200
