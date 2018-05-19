# services/flask/project/tests/test_admin_api_jobs.py

import json
import unittest
from datetime import date, timedelta
import sys

from project.tests.base import BaseTestCase
from project.admin.models import Job
from project.tests.utils import add_job, add_user


class TestAdminApiJobs(BaseTestCase):
    """Tests for the /admin/jobs routes of the Admin Api Service."""

    # Get the dates for yesterday and today
    yesterday = (date.today() - timedelta(1)).isoformat()
    today = date.today().isoformat()

    # Get the first valid option from each enumeration
    VALID_PAID_TO = next(option.value for option in Job.PaidTo)
    VALID_WORKED_BY = next(option.value for option in Job.WorkedBy)
    VALID_CONFIRMATION = next(option.value for option in Job.Confirmation)

    # Create a dictionary for a valid user
    VALID_USER_DICT1 = {
        'username': 'testUser1',
        'email': 'user1@email.com',
        'password': 'somePassword'
    }

    def test_add_job(self):
        """
        Ensure a new job can be added to the database. The client is only
        allowed to create a new job if they are logged in as a user.
        """
        # Add a user to the db
        add_user(**self.VALID_USER_DICT1)

        with self.client:

            # login as user
            login_response = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': self.VALID_USER_DICT1['username'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(login_response.data.decode())['auth_token']

            # a dictionary that represents the job to be added
            job = {
                'client': 'Test Client',
                'description': 'Test Description',
                'amountPaid': 666.01,
                'paidTo': self.VALID_PAID_TO,
                'workedBy': self.VALID_WORKED_BY,
                'confirmation': self.VALID_CONFIRMATION,
                'hasPaid': False,
                'startDate': self.today,
                'endDate': self.today
            }

            # Attempt to add a job to the database
            add_job_response = self.client.post(
                '/admin/jobs',
                data=json.dumps(job),
                headers={'Authorization': f'Bearer {token}'},
                content_type='application/json',
            )
            data = json.loads(add_job_response.data.decode())
            self.assertEqual(add_job_response.status_code, 201)
            self.assertIn('Test Client job was added!', data['message'])
            self.assertIn('success', data['status'])

            # Before comparing the returned job to the job we sent in the
            # request, we need to pop the id off of the returned job.
            self.assertEqual(1, data['job'].pop('id'))

            # The returned job and the input job should now match.
            self.assertEqual(data['job'], job)

    def test_add_jobs_with_valid_paidTo_vals(self):
        """Ensure jobs with valid paidTo values can be added to the db"""
        # Add a user to the db
        add_user(**self.VALID_USER_DICT1)

        for valid_paidTo_val in [t.value for t in Job.PaidTo]:
            with self.client:

                # login as user
                login_response = self.client.post(
                    '/admin/login',
                    data=json.dumps({
                        'username': self.VALID_USER_DICT1['username'],
                        'password': self.VALID_USER_DICT1['password']
                    }),
                    content_type='application/json'
                )

                # get the user's auth token
                token = json.loads(login_response.data.decode())['auth_token']

                add_job_response = self.client.post(
                    '/admin/jobs',
                    data=json.dumps({
                        'client': valid_paidTo_val,
                        'description': 'Test Description',
                        'amountPaid': 666.01,
                        'paidTo': valid_paidTo_val,
                        'workedBy': self.VALID_WORKED_BY,
                        'confirmation': self.VALID_CONFIRMATION,
                        'hasPaid': True,
                        'startDate': self.today,
                        'endDate': self.today
                    }),
                    headers={'Authorization': f'Bearer {token}'},
                    content_type='application/json',
                )
                data = json.loads(add_job_response.data.decode())
                self.assertEqual(add_job_response.status_code, 201)
                self.assertIn(valid_paidTo_val + ' job was added!',
                              data['message'])
                self.assertIn('success', data['status'])

    def test_add_job_with_invalid_paidTo_val(self):
        """Ensure a job with an invalid paidTo value cannot be added."""
        # Add a user to the db
        add_user(**self.VALID_USER_DICT1)

        with self.client:
            # login as user
            login_response = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': self.VALID_USER_DICT1['username'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(login_response.data.decode())['auth_token']

            add_job_response = self.client.post(
                '/admin/jobs',
                data=json.dumps({
                    'client': 'Test Client',
                    'description': 'Test Description',
                    'amountPaid': 666.01,
                    'paidTo': 'INVALID!!!!',
                    'workedBy': self.VALID_WORKED_BY,
                    'confirmation': self.VALID_CONFIRMATION,
                    'hasPaid': False,
                    'startDate': self.today,
                    'endDate': self.today
                }),
                headers={'Authorization': f'Bearer {token}'},
                content_type='application/json',
            )
            data = json.loads(add_job_response.data.decode())
            self.assertEqual(add_job_response.status_code, 400)
            err_msg = ("Invalid 'paidTo' value. " +
                       "The valid values for 'paidTo' are: " +
                       ', '.join([f"'{t.value}'" for t in Job.PaidTo]))
            self.assertEqual(err_msg, data['message'])
            self.assertIn('fail', data['status'])

    def test_add_jobs_with_valid_workedBy_vals(self):
        """Ensure jobs with valid workedBy values can be added to the db"""
        # Add a user to the db
        add_user(**self.VALID_USER_DICT1)

        for valid_workedBy_val in [t.value for t in Job.WorkedBy]:
            with self.client:
                # login as user
                login_response = self.client.post(
                    '/admin/login',
                    data=json.dumps({
                        'username': self.VALID_USER_DICT1['username'],
                        'password': self.VALID_USER_DICT1['password']
                    }),
                    content_type='application/json'
                )

                # get the user's auth token
                token = json.loads(login_response.data.decode())['auth_token']

                add_job_response = self.client.post(
                    '/admin/jobs',
                    data=json.dumps({
                        'client': valid_workedBy_val,
                        'description': 'Test Description',
                        'amountPaid': 666.01,
                        'paidTo': self.VALID_PAID_TO,
                        'workedBy': valid_workedBy_val,
                        'confirmation': self.VALID_CONFIRMATION,
                        'hasPaid': False,
                        'startDate': self.today,
                        'endDate': self.today
                    }),
                    headers={'Authorization': f'Bearer {token}'},
                    content_type='application/json',
                )
                data = json.loads(add_job_response.data.decode())
                self.assertEqual(add_job_response.status_code, 201)
                self.assertIn(valid_workedBy_val + ' job was added!',
                              data['message'])
                self.assertIn('success', data['status'])

    def test_add_job_with_invalid_workedBy_val(self):
        """Ensure a job with an invalid confirmation cannot be added."""
        # Add a user to the db
        add_user(**self.VALID_USER_DICT1)

        with self.client:
            # login as user
            login_response = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': self.VALID_USER_DICT1['username'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(login_response.data.decode())['auth_token']

            add_job_response = self.client.post(
                '/admin/jobs',
                data=json.dumps({
                    'client': 'Test Client',
                    'description': 'Test Description',
                    'amountPaid': 666.01,
                    'paidTo': self.VALID_PAID_TO,
                    'workedBy': 'INVALID!!!',
                    'confirmation': self.VALID_CONFIRMATION,
                    'hasPaid': False,
                    'startDate': self.today,
                    'endDate': self.today
                }),
                headers={'Authorization': f'Bearer {token}'},
                content_type='application/json',
            )
            data = json.loads(add_job_response.data.decode())
            self.assertEqual(add_job_response.status_code, 400)
            err_msg = ("Invalid 'workedBy' value. " +
                       "The valid values for 'workedBy' are: " +
                       ', '.join([f"'{t.value}'" for t in Job.WorkedBy]))
            self.assertEqual(err_msg, data['message'])
            self.assertIn('fail', data['status'])

    def test_add_jobs_with_valid_confirmation_vals(self):
        """Ensure jobs with valid confirmation values can be added to the db"""
        # Add a user to the db
        add_user(**self.VALID_USER_DICT1)

        for valid_confirmation_val in [t.value for t in Job.Confirmation]:
            with self.client:
                # login as user
                login_response = self.client.post(
                    '/admin/login',
                    data=json.dumps({
                        'username': self.VALID_USER_DICT1['username'],
                        'password': self.VALID_USER_DICT1['password']
                    }),
                    content_type='application/json'
                )

                # get the user's auth token
                token = json.loads(login_response.data.decode())['auth_token']

                add_job_response = self.client.post(
                    '/admin/jobs',
                    data=json.dumps({
                        'client': 'Client ' + valid_confirmation_val,
                        'description': 'Test Description',
                        'amountPaid': 666.01,
                        'paidTo': self.VALID_PAID_TO,
                        'workedBy': self.VALID_WORKED_BY,
                        'confirmation': valid_confirmation_val,
                        'hasPaid': False,
                        'startDate': self.today,
                        'endDate': self.today
                    }),
                    headers={'Authorization': f'Bearer {token}'},
                    content_type='application/json',
                )
                data = json.loads(add_job_response.data.decode())
                self.assertEqual(add_job_response.status_code, 201)
                self.assertIn(valid_confirmation_val + ' job was added!',
                              data['message'])
                self.assertIn('success', data['status'])

    def test_add_job_with_invalid_confirmation_val(self):
        """Ensure a job with an invalid confirmation cannot be added."""
        # Add a user to the db
        add_user(**self.VALID_USER_DICT1)

        with self.client:
            # login as user
            login_response = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': self.VALID_USER_DICT1['username'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(login_response.data.decode())['auth_token']

            add_job_response = self.client.post(
                '/admin/jobs',
                data=json.dumps({
                    'client': 'Test Client',
                    'description': 'Test Description',
                    'amountPaid': 666.01,
                    'paidTo': self.VALID_PAID_TO,
                    'workedBy': self.VALID_WORKED_BY,
                    'confirmation': 'INVALID!!!!',
                    'hasPaid': False,
                    'startDate': self.today,
                    'endDate': self.today
                }),
                headers={'Authorization': f'Bearer {token}'},
                content_type='application/json',
            )
            data = json.loads(add_job_response.data.decode())
            self.assertEqual(add_job_response.status_code, 400)
            err_msg = ("Invalid 'confirmation' value. " +
                       "The valid values for 'confirmation' are: " +
                       ', '.join([f"'{t.value}'"
                                  for t in Job.Confirmation]))
            self.assertEqual(err_msg, data['message'])
            self.assertIn('fail', data['status'])

    def test_add_job_empty_json(self):
        """Ensure an error is thrown if the JSON object is empty."""
        # Add a user to the db
        add_user(**self.VALID_USER_DICT1)

        with self.client:

            # login as user
            login_response = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': self.VALID_USER_DICT1['username'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(login_response.data.decode())['auth_token']

            add_job_response = self.client.post(
                '/admin/jobs',
                data=json.dumps({}),
                headers={'Authorization': f'Bearer {token}'},
                content_type='application/json',
            )
            data = json.loads(add_job_response.data.decode())
            self.assertEqual(add_job_response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_job_invalid_json_no_client_key(self):
        """Ensure error thrown if JSON object does not have a client key."""
        # Add a user to the db
        add_user(**self.VALID_USER_DICT1)

        with self.client:
            # login as user
            login_response = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': self.VALID_USER_DICT1['username'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(login_response.data.decode())['auth_token']

            add_job_response = self.client.post(
                '/admin/jobs',
                data=json.dumps({
                    'description': 'Test Description',
                    'amountPaid': 666.01,
                    'paidTo': self.VALID_PAID_TO,
                    'workedBy': self.VALID_WORKED_BY,
                    'confirmation': self.VALID_CONFIRMATION,
                    'hasPaid': False,
                    'startDate': self.today,
                    'endDate': self.today
                }),
                headers={'Authorization': f'Bearer {token}'},
                content_type='application/json',
            )
            data = json.loads(add_job_response.data.decode())
            self.assertEqual(add_job_response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_job_amountPaid_not_a_number(self):
        """Ensure error thrown if amountPaid is a non-numeric string"""
        # Add a user to the db
        add_user(**self.VALID_USER_DICT1)

        with self.client:
            # login as user
            login_response = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': self.VALID_USER_DICT1['username'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(login_response.data.decode())['auth_token']

            add_job_response = self.client.post(
                '/admin/jobs',
                data=json.dumps({
                    'client': 'Test Client',
                    'description': 'Test Description',
                    'amountPaid': 'error!',
                    'paidTo': self.VALID_PAID_TO,
                    'workedBy': self.VALID_WORKED_BY,
                    'confirmation': self.VALID_CONFIRMATION,
                    'hasPaid': False,
                    'startDate': self.today,
                    'endDate': self.today
                }),
                headers={'Authorization': f'Bearer {token}'},
                content_type='application/json',
            )
            data = json.loads(add_job_response.data.decode())
            self.assertEqual(add_job_response.status_code, 400)
            self.assertIn("'amountPaid' must be a number.", data['message'])
            self.assertIn('fail', data['status'])

    def test_add_job_startDate_later_than_endDate(self):
        """Ensure error is thrown if startDate later than endDate."""
        # Add a user to the db
        add_user(**self.VALID_USER_DICT1)

        with self.client:
            # login as user
            login_response = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': self.VALID_USER_DICT1['username'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(login_response.data.decode())['auth_token']

            add_job_response = self.client.post(
                '/admin/jobs',
                data=json.dumps({
                    'client': 'Test Client',
                    'description': 'Test Description',
                    'amountPaid': 666.01,
                    'paidTo': self.VALID_PAID_TO,
                    'workedBy': self.VALID_WORKED_BY,
                    'confirmation': self.VALID_CONFIRMATION,
                    'hasPaid': False,
                    'startDate': self.today,
                    'endDate': self.yesterday
                }),
                headers={'Authorization': f'Bearer {token}'},
                content_type='application/json',
            )
            data = json.loads(add_job_response.data.decode())
            self.assertEqual(add_job_response.status_code, 400)
            self.assertIn('endDate must be equal to', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_job_no_auth_token(self):
        """
        Ensure a new job can be added to the database. The client is only
        allowed to create a new job if they are logged in as a user.
        """
        with self.client:
            # Attempt to add a job to the database
            add_job_response = self.client.post(
                '/admin/jobs',
                data=json.dumps({
                    'client': 'Test Client',
                    'description': 'Test Description',
                    'amountPaid': 666.01,
                    'paidTo': self.VALID_PAID_TO,
                    'workedBy': self.VALID_WORKED_BY,
                    'confirmation': self.VALID_CONFIRMATION,
                    'hasPaid': False,
                    'startDate': self.today,
                    'endDate': self.today
                }),
                content_type='application/json',
            )
            data = json.loads(add_job_response.data.decode())
            self.assertEqual(add_job_response.status_code, 401)
            self.assertIn('Provide a valid auth token.', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_single_job(self):
        """Ensure get single job behaves correctly."""
        job = add_job(
                client='Test Client',
                description='Test Description',
                amount_paid=666.01,
                paid_to=self.VALID_PAID_TO,
                worked_by=self.VALID_WORKED_BY,
                confirmation=self.VALID_CONFIRMATION,
                has_paid=False,
                start_date=self.today
        )
        with self.client:
            response = self.client.get(f'/admin/jobs/{job.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Test Client', data['data']['client'])
            self.assertIn('Test Description', data['data']['description'])
            self.assertEqual(666.01, data['data']['amountPaid'])
            self.assertEqual(self.VALID_PAID_TO, data['data']['paidTo'])
            self.assertEqual(self.VALID_WORKED_BY, data['data']['workedBy'])
            self.assertEqual(self.VALID_CONFIRMATION,
                             data['data']['confirmation'])
            self.assertFalse(data['data']['hasPaid'])
            self.assertIn(self.today, data['data']['startDate'])
            self.assertIn(self.today, data['data']['endDate'])
            self.assertIn('success', data['status'])

    def test_get_single_job_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/admin/jobs/blurp')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Job does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_single_job_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/admin/jobs/9999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Job does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_all_jobs(self):
        """Ensure get all jobs behaves correctly."""
        add_job(
                client='Client 1',
                description='Description 1',
                amount_paid=111.11,
                paid_to=self.VALID_PAID_TO,
                worked_by=self.VALID_WORKED_BY,
                confirmation=self.VALID_CONFIRMATION,
                has_paid=False,
                start_date=self.yesterday
        )
        add_job(
                client='Client 2',
                description='Description 2',
                amount_paid=222.22,
                paid_to=self.VALID_PAID_TO,
                worked_by=self.VALID_WORKED_BY,
                confirmation=self.VALID_CONFIRMATION,
                has_paid=True,
                start_date=self.yesterday,
                end_date=self.today
        )
        with self.client:
            response = self.client.get('/admin/jobs')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(len(data['data']['jobs']), 2)
            jobs = data['data']['jobs']
            # Assertions for job 1
            self.assertIn('Client 1', jobs[0]['client'])
            self.assertIn('Description 1', jobs[0]['description'])
            self.assertEqual(111.11, jobs[0]['amountPaid'])
            self.assertEqual(self.VALID_PAID_TO, jobs[0]['paidTo'])
            self.assertEqual(self.VALID_WORKED_BY, jobs[0]['workedBy'])
            self.assertEqual(self.VALID_CONFIRMATION, jobs[0]['confirmation'])
            self.assertFalse(jobs[0]['hasPaid'])
            self.assertEqual(self.yesterday, jobs[0]['startDate'])
            self.assertEqual(self.yesterday, jobs[0]['endDate'])
            # Assertions for job 2
            self.assertIn('Client 2', jobs[1]['client'])
            self.assertIn('Description 2', jobs[1]['description'])
            self.assertEqual(222.22, jobs[1]['amountPaid'])
            self.assertEqual(self.VALID_PAID_TO, jobs[1]['paidTo'])
            self.assertEqual(self.VALID_WORKED_BY, jobs[1]['workedBy'])
            self.assertEqual(self.VALID_CONFIRMATION, jobs[1]['confirmation'])
            self.assertTrue(jobs[1]['hasPaid'])
            self.assertEqual(self.yesterday, jobs[1]['startDate'])
            self.assertEqual(self.today, jobs[1]['endDate'])


if __name__ == '__main__':
    unittest.main()
