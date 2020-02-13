#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 10/4/19 by Pat Blair
"""
Configure the app.

.. currentmodule:: {{cookiecutter.package_name}}.config
.. moduleauthor:: {{cookiecutter.author_name}} <{{cookiecutter.author_email}}>
"""
from pathlib import Path
import os
import tempfile

TRUTHY = ['true']  #: strings that indicate the boolean value ``True``


def is_truthy(s: str) -> bool:
    """
    Returns ``True`` if and only if a ``str`` value is "truthy".

    :param s: the string
    :return: ``True`` if the value is "truthy", otherwise ``False``
    """
    if not s:
        return False
    return s.strip().lower() in TRUTHY


class Defaults:
    """
    These are the default configuration settings.
    """
    DEBUG = False
    TESTING = False


class Config(object):
    """
    This is the base class for configuration objects.
    """
    DEBUG = True if os.environ.get('DEBUG') == 'True' else False
    TESTING = True if os.environ.get('TESTING') == 'True' else False


class ProductionConfig(Config):
    """
    This is the production configuration.
    """
    DEBUG = False


class StagingConfig(Config):
    """
    This is the staging configuration.
    """
    DEBUG = True


class DevelopmentConfig(Config):
    """
    This is the development configuration.
    """
    DEBUG = True


class TestingConfig(Config):
    """
    This is the testing configuration.
    """
    DEBUG = True


def get_name() -> str:
    """
    Get the simple name of the current configuration environment.

    :return: the simple name (*e.g.* 'production', or 'development', *etc.*)
    """
    return os.environ.get('FLASK_ENV', 'production')


def get_object_name() -> str:
    """
    Get the name of the configuration object.

    :return: the fully-qualified name of the configuration object
    """
    return f"{__name__}.{get_name().title()}Config"
