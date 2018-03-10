# services/flask/project/tests/utils.py


from project import db
from project.admin.models import User, Job, OneTimeExpense


def add_user(username, email):
    user = User(username=username, email=email)
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
