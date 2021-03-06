# services/flask/project/tests/utils.py
import re

from project import db
from project.admin.models import User, Job, OneTimeExpense, RecurringExpense


def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def add_job(client, description, amount_paid, paid_to, worked_by,
            confirmation, has_paid, start_date, end_date=None):
    job = Job(client, description, amount_paid, paid_to, worked_by,
              confirmation, has_paid, start_date, end_date)
    db.session.add(job)
    db.session.commit()
    return job


def add_one_time_expense(merchant, description, amount_spent, date, paid_by,
                         tax_deductible, category):
    expense = OneTimeExpense(merchant, description, amount_spent, date,
                             paid_by, tax_deductible, category)
    db.session.add(expense)
    db.session.commit()
    return expense


def add_recurring_expense(merchant, description, amount, tax_deductible,
                          category, recurrence, paid_by, start_date,
                          end_date=None):
    expense = RecurringExpense(merchant, description, amount, tax_deductible,
                               category, recurrence, paid_by, start_date,
                               end_date)
    db.session.add(expense)
    db.session.commit()
    return expense


# Given a dictionary, return an identical dictionary, but with all camelCased
# keys changed to underscored keys
def underscore_keys(inputDict):
    outputDict = {}
    for key, value in inputDict.items():
        outputDict[camelcase_to_underscore(key)] = value
    return outputDict


def camelcase_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
