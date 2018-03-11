# services/flask/project/admin/api.py

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.admin.models import (User, Job, OneTimeExpense, RecurringExpense)
from project import db


admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/ping', methods=['GET'])
def ping():
    """Respond to a ping"""
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


# ==========
# JOB ROUTES
# ==========


@admin_blueprint.route('/jobs', methods=['POST'])
def add_job():
    """Add a job to the database"""
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    post_data = request.get_json()
    if not post_data:
        return jsonify(response_object), 400
    try:
        job = Job(
                   client=post_data.get('client'),
                   description=post_data.get('description'),
                   amount_paid=post_data.get('amount_paid'),
                   paid_to=post_data.get('paid_to'),
                   worked_by=post_data.get('worked_by'),
                   confirmation=post_data.get('confirmation'),
                   has_paid=post_data.get('has_paid'),
                   start_date=post_data.get('start_date'),
                   end_date=post_data.get('end_date'),
        )
        db.session.add(job)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': f'{job.client} job was added!'
        }
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        if job.start_date > job.end_date:
            msg = 'end_date must be equal to or later than start_date'
            response_object['message'] = msg
        return jsonify(response_object), 400
    except exc.DataError as e:
        db.session.rollback()
        err_msg = str(e)
        if 'invalid input syntax for type double precision' in err_msg:
            response_object['message'] = "'amount_paid' must be a number."
        return jsonify(response_object), 400
    except ValueError as e:
        db.session.rollback()
        err_msg = str(e)
        if 'is not a valid PaidTo' in err_msg:
            err_msg = ("Invalid 'paid_to' value. " +
                       "The valid values for 'paid_to' are: " +
                       ', '.join([f"'{t.value}'" for t in Job.PaidTo]))
        elif 'is not a valid WorkedBy' in err_msg:
            err_msg = ("Invalid 'worked_by' value. " +
                       "The valid values for 'worked_by' are: " +
                       ', '.join([f"'{t.value}'" for t in Job.WorkedBy]))
        elif 'is not a valid Confirmation' in err_msg:
            err_msg = ("Invalid 'confirmation' value. " +
                       "The valid values for 'confirmation' are: " +
                       ', '.join([f"'{t.value}'"
                                  for t in Job.Confirmation]))
        response_object['message'] = err_msg
        return jsonify(response_object), 400


@admin_blueprint.route('/jobs/<job_id>', methods=['GET'])
def get_single_job(job_id):
    """Get single job details"""
    response_object = {
        'status': 'fail',
        'message': 'Job does not exist'
    }
    try:
        job = Job.query.filter_by(id=job_id).first()
        if not job:
            return jsonify(response_object), 404
        response_object = {
                'status': 'success',
                'data': job.to_json()
        }
        return jsonify(response_object), 200
    except (ValueError, exc.DataError):
        return jsonify(response_object), 404


@admin_blueprint.route('/jobs', methods=['GET'])
def get_all_jobs():
    """Get all jobs"""
    response_object = {
        'status': 'success',
        'data': {
            'jobs': [job.to_json() for job in Job.query.all()]
        }
    }
    return jsonify(response_object), 200


# =======================
# ONE TIME EXPENSE ROUTES
# =======================


@admin_blueprint.route('/one-time-expenses', methods=['POST'])
def add_one_time_expense():
    """Add a one time expense to the database"""
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    post_data = request.get_json()
    if not post_data:
        return jsonify(response_object), 400
    try:
        expense = OneTimeExpense(
                              merchant=post_data.get('merchant'),
                              description=post_data.get('description'),
                              amount_spent=post_data.get('amount_spent'),
                              date=post_data.get('date'),
                              paid_by=post_data.get('paid_by'),
                              tax_deductible=post_data.get('tax_deductible'),
                              category=post_data.get('category')
        )
        db.session.add(expense)
        db.session.commit()
        response_object = {
                'status': 'success',
                'message': f'{post_data.get("merchant")} expense was added!'
        }
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400
    except exc.DataError as e:
        db.session.rollback()
        err_msg = str(e)
        if 'invalid input syntax for type double precision' in err_msg:
            response_object['message'] = "'amount_spent' must be a number."
        return jsonify(response_object), 400
    except ValueError as e:
        db.session.rollback()
        err_msg = str(e)
        if 'is not a valid Category' in err_msg:
            err_msg = ("Invalid 'category' value. " +
                       "The valid values for 'category' are: " +
                       ', '.join([f"'{t.value}'"
                                  for t in OneTimeExpense.Category]))
        if 'is not a valid PaidBy' in err_msg:
            err_msg = ("Invalid 'paid_by' value. " +
                       "The valid values for 'paid_by' are: " +
                       ', '.join([f"'{t.value}'"
                                  for t in OneTimeExpense.PaidBy]))
        response_object['message'] = err_msg
        return jsonify(response_object), 400


@admin_blueprint.route('/one-time-expenses/<expense_id>', methods=['GET'])
def get_single_one_time_expense(expense_id):
    """Get single one time expense"""
    response_object = {
        'status': 'fail',
        'message': 'Expense does not exist'
    }
    try:
        expense = OneTimeExpense.query.filter_by(id=int(expense_id)).first()
        if not expense:
            return jsonify(response_object), 404
        response_object = {
                            'status': 'success',
                            'data': expense.to_json()
        }
        return jsonify(response_object), 200
    except (ValueError, exc.DataError):
        return jsonify(response_object), 404


@admin_blueprint.route('/one-time-expenses', methods=['GET'])
def get_all_one_time_expenses():
    """Get all one time expenses"""
    expenses = OneTimeExpense.query.all()
    response_object = {
            'status': 'success',
            'data': {
                      'one-time-expenses': [expense.to_json()
                                            for expense in expenses]
                    }
    }
    return jsonify(response_object), 200


# ========================
# RECURRING EXPENSE ROUTES
# ========================


@admin_blueprint.route('/recurring-expenses', methods=['POST'])
def add_recurring_expense():
    """Add a recurring expense to the database"""
    response_object = {
                        'status': 'fail',
                        'message': 'Invalid payload.'
    }
    post_data = request.get_json()
    if not post_data:
        return jsonify(response_object), 400
    try:
        expense = RecurringExpense(
                                merchant=post_data.get('merchant'),
                                description=post_data.get('description'),
                                amount=post_data.get('amount'),
                                tax_deductible=post_data.get('tax_deductible'),
                                category=post_data.get('category'),
                                recurrence=post_data.get('recurrence'),
                                paid_by=post_data.get('paid_by'),
                                start_date=post_data.get('start_date'),
                                end_date=post_data.get('end_date')
        )
        db.session.add(expense)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': f'{expense.merchant} recurring expense was added!'
        }
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        if 'violates check constraint' in str(e):
            msg = 'start_date must be earlier than end_date'
            response_object['message'] = msg
        return jsonify(response_object), 400
    except ValueError as e:
        db.session.rollback()
        err_msg = str(e)
        if 'is not a valid Recurrence' in err_msg:
            err_msg = ("Invalid 'recurrence' value. " +
                       "The valid values for 'recurrence' are: " +
                       ', '.join([f"'{t.value}'"
                                  for t in RecurringExpense.Recurrence]))
        if 'is not a valid PaidBy' in err_msg:
            err_msg = ("Invalid 'paid_by' value. " +
                       "The valid values for 'paid_by' are: " +
                       ', '.join([f"'{t.value}'"
                                  for t in RecurringExpense.PaidBy]))
        if 'is not a valid Category' in err_msg:
            err_msg = ("Invalid 'category' value. " +
                       "The valid values for 'category' are: " +
                       ', '.join([f"'{t.value}'"
                                  for t in RecurringExpense.Category]))
        response_object['message'] = err_msg
        return jsonify(response_object), 400


@admin_blueprint.route('/recurring-expenses/<expense_id>', methods=['GET'])
def get_single_recurring_expense(expense_id):
    response_object = {
        'status': 'fail',
        'message': 'Expense does not exist'
    }
    try:
        expense = RecurringExpense.query.filter_by(id=int(expense_id)).first()
        if not expense:
            return jsonify(response_object), 404
        response_object = {
                            'status': 'success',
                            'data': expense.to_json()
        }
        return jsonify(response_object), 200
    except (ValueError, exc.DataError):
        return jsonify(response_object), 404


@admin_blueprint.route('/recurring-expenses', methods=['GET'])
def get_all_recurring_expenses():
    """Get all recurring expenses"""
    expenses = RecurringExpense.query.all()
    response_object = {
            'status': 'success',
            'data': {
                      'recurring-expenses': [expense.to_json()
                                             for expense in expenses]
                    }
    }
    return jsonify(response_object), 200


# ===========
# USER ROUTES
# ===========


@admin_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    try:
        email = post_data.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(username=post_data.get('username'),
                        email=email,
                        password=post_data.get('password')
            )
            db.session.add(user)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'User {user.username} was added!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That email already exists.'
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return jsonify(response_object), 400


@admin_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get single user details"""
    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                                'status': 'success',
                                'data': user.to_json()
                              }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@admin_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    response_object = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }
    return jsonify(response_object), 200
