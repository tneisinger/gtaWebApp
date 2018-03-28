# services/flask/manage.py

import unittest
import coverage
import click
from flask.cli import FlaskGroup

from project import create_app, db
from project.admin.models import User


COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
    ]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def test_narrow():
    """ Runs the tests without code coverage"""
    PATTERN = 'test_admin_calendar.py'
    click.echo('Running only the subset of tests that match this pattern:')
    click.echo(f'PATTERN: {PATTERN}')
    click.echo('To change the pattern, edit the manage.py file.')
    tests = unittest.TestLoader().discover('project/tests', pattern=PATTERN)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def seed_db():
    """Seeds the database."""
    db.session.add(User(
        username='Tyler',
        email='tjneisi@gmail.com',
        password='somepassword'
    ))
    db.session.add(User(
        username='Meghan',
        email="meghanunderwood8@gmail.com",
        password='somepassword'
    ))
    db.session.commit()

@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1

if __name__ == '__main__':
    cli()
