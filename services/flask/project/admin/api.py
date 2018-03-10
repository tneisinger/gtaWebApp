# services/flask/project/admin/api.py

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.admin.models import (User, Job, JobPaidToOption,
                                  JobWorkedByOption, JobConfirmationOption)
from project import db


admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/ping', methods=['GET'])
def ping():
    """Respond to a ping"""
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


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
        if 'is not a valid JobPaidToOption' in err_msg:
            err_msg = ("Invalid 'paid_to' value. " +
                       "The valid values for 'paid_to' are: " +
                       ', '.join([f"'{t.value}'" for t in JobPaidToOption]))
        elif 'is not a valid JobWorkedByOption' in err_msg:
            err_msg = ("Invalid 'worked_by' value. " +
                       "The valid values for 'worked_by' are: " +
                       ', '.join([f"'{t.value}'" for t in JobWorkedByOption]))
        elif 'is not a valid JobConfirmationOption' in err_msg:
            err_msg = ("Invalid 'confirmation' value. " +
                       "The valid values for 'confirmation' are: " +
                       ', '.join([f"'{t.value}'"
                                  for t in JobConfirmationOption]))
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
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'active': user.active
                }
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
