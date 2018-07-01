# services/flask/project/admin/api.py

from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_

from project.admin.models import (User, Job, OneTimeExpense, RecurringExpense)
from project import db, bcrypt
from project.admin.decorators import users_only

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
@users_only()
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
                   amount_paid=post_data.get('amountPaid'),
                   paid_to=post_data.get('paidTo'),
                   worked_by=post_data.get('workedBy'),
                   confirmation=post_data.get('confirmation'),
                   has_paid=post_data.get('hasPaid'),
                   start_date=post_data.get('startDate'),
                   end_date=post_data.get('endDate'),
        )
        db.session.add(job)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': f'{job.client} job was added!',
            'job': job.to_json()
        }
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        if job.start_date > job.end_date:
            msg = 'endDate must be equal to or later than startDate'
            response_object['message'] = msg
        return jsonify(response_object), 400
    except exc.DataError as e:
        db.session.rollback()
        err_msg = str(e)
        if 'invalid input syntax for type double precision' in err_msg:
            response_object['message'] = "'amountPaid' must be a number."
        return jsonify(response_object), 400
    except ValueError as e:
        db.session.rollback()
        err_msg = str(e)
        if 'is not a valid PaidTo' in err_msg:
            err_msg = ("Invalid 'paidTo' value. " +
                       "The valid values for 'paidTo' are: " +
                       ', '.join([f"'{t.value}'" for t in Job.PaidTo]))
        elif 'is not a valid WorkedBy' in err_msg:
            err_msg = ("Invalid 'workedBy' value. " +
                       "The valid values for 'workedBy' are: " +
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


@admin_blueprint.route('/jobs/<job_id>', methods=['POST'])
def update_job(job_id):
    """Update the details of an existing job"""
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    post_data = request.get_json()
    if not post_data:
        return jsonify(response_object), 400
    response_object = {
        'status': 'fail',
        'message': 'Job does not exist'
    }
    try:
        job = Job.query.filter_by(id=job_id).first()
        if not job:
            return jsonify(response_object), 404
        updated_job = Job(
                   client=post_data.get('client'),
                   description=post_data.get('description'),
                   amount_paid=post_data.get('amountPaid'),
                   paid_to=post_data.get('paidTo'),
                   worked_by=post_data.get('workedBy'),
                   confirmation=post_data.get('confirmation'),
                   has_paid=post_data.get('hasPaid'),
                   start_date=post_data.get('startDate'),
                   end_date=post_data.get('endDate'),
        )
        job.client = updated_job.client
        job.description = updated_job.description
        job.amount_paid = updated_job.amount_paid
        job.paid_to = updated_job.paid_to
        job.worked_by = updated_job.worked_by
        job.confirmation = updated_job.confirmation
        job.has_paid = updated_job.has_paid
        job.start_date = updated_job.start_date
        job.end_date = updated_job.end_date
        db.session.commit()
        response_object = {
                'status': 'success',
                'data': job.to_json(),
                'message': 'Job updated successfully',
                'job': job.to_json()
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
                              amount_spent=post_data.get('amountSpent'),
                              date=post_data.get('date'),
                              paid_by=post_data.get('paidBy'),
                              tax_deductible=post_data.get('taxDeductible'),
                              category=post_data.get('category')
        )
        db.session.add(expense)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': f'{post_data.get("merchant")} expense was added!',
            'expense': expense.to_json()
        }
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400
    except exc.DataError as e:
        db.session.rollback()
        err_msg = str(e)
        if 'invalid input syntax for type double precision' in err_msg:
            response_object['message'] = "'amountSpent' must be a number."
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
            err_msg = ("Invalid 'paidBy' value. " +
                       "The valid values for 'paidBy' are: " +
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
                                tax_deductible=post_data.get('taxDeductible'),
                                category=post_data.get('category'),
                                recurrence=post_data.get('recurrence'),
                                paid_by=post_data.get('paidBy'),
                                start_date=post_data.get('startDate'),
                                end_date=post_data.get('endDate')
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
            err_msg = ("Invalid 'paidBy' value. " +
                       "The valid values for 'paidBy' are: " +
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
                        password=post_data.get('password'))
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


# ===========
# AUTH ROUTES
# ===========


@admin_blueprint.route('/register', methods=['POST'])
def register_user():
    """Register a new user"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    is_private_device = post_data.get('isPrivateDevice')
    try:
        # check for existing user
        user = User.query.filter(
            or_(User.username == username, User.email == email)).first()
        if not user:
            # add new user to db
            new_user = User(
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            # generate auth token
            (auth_token, exp) = new_user.encode_auth_token(new_user.id,
                                                           is_private_device)
            response_object['status'] = 'success'
            response_object['message'] = 'Successfully registered.'
            response_object['expiration'] = exp
            response_object['auth_token'] = auth_token.decode()
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That user already exists.'
            return jsonify(response_object), 400
    # handler errors
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return jsonify(response_object), 400


@admin_blueprint.route('/login', methods=['POST'])
def login_user():
    # get post data
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    username = post_data.get('username')
    password = post_data.get('password')
    is_private_device = post_data.get('isPrivateDevice')
    try:
        # fetch the user data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            (auth_token, exp) = user.encode_auth_token(user.id,
                                                       is_private_device)
            if auth_token:
                response_object['user'] = {
                        'username': user.username
                }
                response_object['status'] = 'success'
                response_object['message'] = 'Successfully logged in.'
                response_object['expiration'] = exp
                response_object['auth_token'] = auth_token.decode()
                return jsonify(response_object), 200
        else:
            response_object['message'] = 'User does not exist.'
            return jsonify(response_object), 404
    except Exception as e:
        response_object['message'] = 'Try again.'
        return jsonify(response_object), 500


@admin_blueprint.route('/logout', methods=['GET'])
def logout_user():
    # get auth token
    auth_header = request.headers.get('Authorization')
    response_object = {
        'status': 'fail',
        'message': 'Provide a valid auth token.'
    }
    if auth_header:
        auth_token = auth_header.split(' ')[1]
        decode_response, _ = User.decode_auth_token(auth_token)
        if not isinstance(decode_response, str):
            response_object['status'] = 'success'
            response_object['message'] = 'Successfully logged out.'
            return jsonify(response_object), 200
        else:
            response_object['message'] = decode_response
            return jsonify(response_object), 401
    else:
        return jsonify(response_object), 403


@admin_blueprint.route('/status', methods=['GET'])
def get_user_status():
    # get auth token
    auth_header = request.headers.get('Authorization')
    response_object = {
        'status': 'fail',
        'message': 'Provide a valid auth token.'
    }
    if auth_header:
        auth_token = auth_header.split(' ')[1]
        decode_response, exp = User.decode_auth_token(auth_token)
        if not isinstance(decode_response, str):
            user = User.query.filter_by(id=decode_response).first()
            response_object['status'] = 'success'
            response_object['message'] = 'Success.'
            response_object['expiration'] = exp
            response_object['user'] = user.to_json()
            return jsonify(response_object), 200
        response_object['message'] = decode_response
        return jsonify(response_object), 401
    else:
        return jsonify(response_object), 401


# ==========================
# CALENDAR AND BUDGET ROUTES
# ==========================


@admin_blueprint.route('/events', methods=['GET'])
@users_only(pass_user=True)
def get_events(user):
    """Get jobs and one time expenses from within a date range"""
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    jobs = Job.query.filter(
            Job.end_date >= start_date,
            Job.start_date <= end_date).all()
    expenses = OneTimeExpense.query.filter(
            OneTimeExpense.date >= start_date,
            OneTimeExpense.date <= end_date).all()
    response_object = {
        'status': 'success',
        'data': {
            'jobs': [j.to_json() for j in jobs],
            'expenses': [e.to_json() for e in expenses],
            'user': user.to_json()
        }
    }
    return jsonify(response_object), 200
