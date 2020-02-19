#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.  It
can be used as a handy facility for running the task from a command line.

.. currentmodule:: {{cookiecutter.package_name}}
.. moduleauthor:: {{cookiecutter.author_name}} <{{cookiecutter.author_email}}>

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.
"""
import logging
import os
import click
from .__init__ import __version__
from .app import initdb

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


class Info(object):
    """
    An information object to pass data between CLI functions.
    """

    def __init__(self):  # Note: This object must have an empty constructor.
        self.verbose: int = 0


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)


# Change the options to below to suit the actual options for your task (or
# tasks).
@click.group()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@pass_info
def cli(info: Info, verbose: int):
    """
    Run the {{cookiecutter.project_name}} REST API.
    """
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    info.verbose = verbose


# pylint: disable=too-many-arguments
@cli.command()
@click.option(
    '--flask-env', '-f', 'flask_env',
    type=click.Choice([
        'production',
        'staging',
        'development',
        'testing'
    ]),
    envvar='FLASK_ENV',
    default='production',
    help="the Flask environment"
)
@click.option(
    '--static-folder', '-s', 'static_folder',
    type=click.Path(exists=True),
    envvar='STATIC_FOLDER',
    default=None,
    help="the Flask static file path"
)
@click.option(
    '--host', '-h',
    type=str,
    default='0.0.0.0',
    help='the host on which the API listens'
)
@click.option(
    '--port', '-p',
    type=int,
    default=4000,
    help='the port on which the API listens'
)
@click.option(
    '--flask-workers', '-w', 'flask_workers',
    type=int,
    default=4,
    help='the number of Flask worker processes'
)
@click.option(
    '--timeout', '-t',
    type=int,
    default=800,
    help=(
        'the maximum time (in seconds) a worker may be silent before '
        'being restarted'
    )
)
@click.option(
    '--dburi', '-d',
    type=str,
    help='the database URI'
)
@pass_info
def run(
        info: Info,
        flask_env: str,
        static_folder: str,
        host: str,
        port: int,
        flask_workers: int,
        timeout: int,
        dburi: str
):
    """
    Run the server.
    """
    # ------------- ENVIRONMENT VARIABLES -------------

    # Set FLASK environment variables from the arguments.
    if flask_env:
        os.environ['FLASK_ENV'] = flask_env
    if static_folder:
        os.environ['STATIC_FOLDER'] = static_folder
    # Set SQLAlchemy envrionment variables from the arguments.
    if dburi:
        os.environ['SQLALCHEMY_DATABASE_URI'] = dburi

    # ---------------- PRE-FLIGHT CHECK ----------------

    # Perform any additional tasks that are required before starting the
    # Flask application.

    initdb()

    # ------------------ START FLASK -------------------

    # Prepare the `gunicorn` command.
    cmd = (
        f"gunicorn -w {flask_workers} "
        f"-b {host}:{port} "
        f"--timeout {timeout} "
        f"{{cookiecutter.package_name}}.app:app"
    )

    # Show the command to the user.
    click.echo(click.style(cmd, fg='blue'))
    # Let's go!
    os.system(cmd)


@cli.command()
def version():
    """
    Get the library version.
    """
    click.echo(click.style(f"{__version__}", bold=True))
