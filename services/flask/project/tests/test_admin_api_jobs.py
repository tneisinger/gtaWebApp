# services/flask/project/tests/test_admin_api_jobs.py

import json
from datetime import date, timedelta

from project.tests.base import BaseTestCase
from project.admin.models import (JobWorkedByOption, JobConfirmationOption,
                                  JobPaidToOption)
from project.tests.utils import add_job


class TestAdminApiJobs(BaseTestCase):
    """Tests for the /admin/jobs routes of the Admin Api Service."""

    # Get the dates for yesterday and today
    yesterday = (date.today() - timedelta(1)).isoformat()
    today = date.today().isoformat()

    # Get the first valid option from each enumeration
    VALID_PAID_TO = next(option.value for option in JobPaidToOption)
    VALID_WORKED_BY = next(option.value for option in JobWorkedByOption)
    VALID_CONFIRMATION = next(option.value for option in JobConfirmationOption)

    def test_add_job(self):
        """Ensure a new job can be added to the database."""
        with self.client:
            response = self.client.post(
                '/admin/jobs',
                data=json.dumps({
                    'client': 'Test Client',
                    'description': 'Test Description',
                    'amount_paid': 666.01,
                    'paid_to': self.VALID_PAID_TO,
                    'worked_by': self.VALID_WORKED_BY,
                    'confirmation': self.VALID_CONFIRMATION,
                    'has_paid': False,
                    'start_date': self.today,
                    'end_date': self.today
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Test Client job was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_jobs_with_valid_paid_to_vals(self):
        """Ensure jobs with valid paid_to values can be added to the db"""
        for valid_paid_to_val in [t.value for t in JobPaidToOption]:
            with self.client:
                response = self.client.post(
                    '/admin/jobs',
                    data=json.dumps({
                        'client': valid_paid_to_val,
                        'description': 'Test Description',
                        'amount_paid': 666.01,
                        'paid_to': valid_paid_to_val,
                        'worked_by': self.VALID_WORKED_BY,
                        'confirmation': self.VALID_CONFIRMATION,
                        'has_paid': True,
                        'start_date': self.today,
                        'end_date': self.today
                    }),
                    content_type='application/json',
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)
                self.assertIn(valid_paid_to_val + ' job was added!',
                              data['message'])
                self.assertIn('success', data['status'])

    def test_add_job_with_invalid_paid_to_val(self):
        """Ensure a job with an invalid paid_to value cannot be added."""
        with self.client:
            response = self.client.post(
                '/admin/jobs',
                data=json.dumps({
                    'client': 'Test Client',
                    'description': 'Test Description',
                    'amount_paid': 666.01,
                    'paid_to': 'INVALID!!!!',
                    'worked_by': self.VALID_WORKED_BY,
                    'confirmation': self.VALID_CONFIRMATION,
                    'has_paid': False,
                    'start_date': self.today,
                    'end_date': self.today
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            err_msg = ("Invalid 'paid_to' value. " +
                       "The valid values for 'paid_to' are: " +
                       ', '.join([f"'{t.value}'" for t in JobPaidToOption]))
            self.assertEqual(err_msg, data['message'])
            self.assertIn('fail', data['status'])

    def test_add_jobs_with_valid_worked_by_vals(self):
        """Ensure jobs with valid worked_by values can be added to the db"""
        for valid_worked_by_val in [t.value for t in JobWorkedByOption]:
            with self.client:
                response = self.client.post(
                    '/admin/jobs',
                    data=json.dumps({
                        'client': valid_worked_by_val,
                        'description': 'Test Description',
                        'amount_paid': 666.01,
                        'paid_to': self.VALID_PAID_TO,
                        'worked_by': valid_worked_by_val,
                        'confirmation': self.VALID_CONFIRMATION,
                        'has_paid': False,
                        'start_date': self.today,
                        'end_date': self.today
                    }),
                    content_type='application/json',
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)
                self.assertIn(valid_worked_by_val + ' job was added!',
                              data['message'])
                self.assertIn('success', data['status'])

    def test_add_job_with_invalid_worked_by_val(self):
        """Ensure a job with an invalid confirmation cannot be added."""
        with self.client:
            response = self.client.post(
                '/admin/jobs',
                data=json.dumps({
                    'client': 'Test Client',
                    'description': 'Test Description',
                    'amount_paid': 666.01,
                    'paid_to': self.VALID_PAID_TO,
                    'worked_by': 'INVALID!!!',
                    'confirmation': self.VALID_CONFIRMATION,
                    'has_paid': False,
                    'start_date': self.today,
                    'end_date': self.today
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            err_msg = ("Invalid 'worked_by' value. " +
                       "The valid values for 'worked_by' are: " +
                       ', '.join([f"'{t.value}'" for t in JobWorkedByOption]))
            self.assertEqual(err_msg, data['message'])
            self.assertIn('fail', data['status'])

    def test_add_jobs_with_valid_confirmation_vals(self):
        """Ensure jobs with valid confirmation values can be added to the db"""
        for valid_confirmation_val in [t.value for t in JobConfirmationOption]:
            with self.client:
                response = self.client.post(
                    '/admin/jobs',
                    data=json.dumps({
                        'client': 'Client ' + valid_confirmation_val,
                        'description': 'Test Description',
                        'amount_paid': 666.01,
                        'paid_to': self.VALID_PAID_TO,
                        'worked_by': self.VALID_WORKED_BY,
                        'confirmation': valid_confirmation_val,
                        'has_paid': False,
                        'start_date': self.today,
                        'end_date': self.today
                    }),
                    content_type='application/json',
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)
                self.assertIn(valid_confirmation_val + ' job was added!',
                              data['message'])
                self.assertIn('success', data['status'])

    def test_add_job_with_invalid_confirmation_val(self):
        """Ensure a job with an invalid confirmation cannot be added."""
        with self.client:
            response = self.client.post(
                '/admin/jobs',
                data=json.dumps({
                    'client': 'Test Client',
                    'description': 'Test Description',
                    'amount_paid': 666.01,
                    'paid_to': self.VALID_PAID_TO,
                    'worked_by': self.VALID_WORKED_BY,
                    'confirmation': 'INVALID!!!!',
                    'has_paid': False,
                    'start_date': self.today,
                    'end_date': self.today
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            err_msg = ("Invalid 'confirmation' value. " +
                       "The valid values for 'confirmation' are: " +
                       ', '.join([f"'{t.value}'"
                                  for t in JobConfirmationOption]))
            self.assertEqual(err_msg, data['message'])
            self.assertIn('fail', data['status'])

    def test_add_job_empty_json(self):
        """Ensure an error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/admin/jobs',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_job_invalid_json_no_client_key(self):
        """Ensure error thrown if JSON object does not have a client key."""
        with self.client:
            response = self.client.post(
                '/admin/jobs',
                data=json.dumps({
                    'description': 'Test Description',
                    'amount_paid': 666.01,
                    'paid_to': self.VALID_PAID_TO,
                    'worked_by': self.VALID_WORKED_BY,
                    'confirmation': self.VALID_CONFIRMATION,
                    'has_paid': False,
                    'start_date': self.today,
                    'end_date': self.today
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_job_amount_paid_not_a_number(self):
        """Ensure error thrown if amount_paid is a non-numeric string"""
        with self.client:
            response = self.client.post(
                '/admin/jobs',
                data=json.dumps({
                    'client': 'Test Client',
                    'description': 'Test Description',
                    'amount_paid': 'error!',
                    'paid_to': self.VALID_PAID_TO,
                    'worked_by': self.VALID_WORKED_BY,
                    'confirmation': self.VALID_CONFIRMATION,
                    'has_paid': False,
                    'start_date': self.today,
                    'end_date': self.today
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("'amount_paid' must be a number.", data['message'])
            self.assertIn('fail', data['status'])

    def test_add_job_start_date_later_than_end_date(self):
        """Ensure error is thrown if start_date later than end_date."""
        with self.client:
            response = self.client.post(
                '/admin/jobs',
                data=json.dumps({
                    'client': 'Test Client',
                    'description': 'Test Description',
                    'amount_paid': 666.01,
                    'paid_to': self.VALID_PAID_TO,
                    'worked_by': self.VALID_WORKED_BY,
                    'confirmation': self.VALID_CONFIRMATION,
                    'has_paid': False,
                    'start_date': self.today,
                    'end_date': self.yesterday
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('end_date must be equal to', data['message'])
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
            self.assertEqual(666.01, data['data']['amount_paid'])
            self.assertEqual(self.VALID_PAID_TO, data['data']['paid_to'])
            self.assertEqual(self.VALID_WORKED_BY, data['data']['worked_by'])
            self.assertEqual(self.VALID_CONFIRMATION,
                             data['data']['confirmation'])
            self.assertFalse(data['data']['has_paid'])
            self.assertIn(self.today, data['data']['start_date'])
            self.assertIn(self.today, data['data']['end_date'])
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
            self.assertEqual(111.11, jobs[0]['amount_paid'])
            self.assertEqual(self.VALID_PAID_TO, jobs[0]['paid_to'])
            self.assertEqual(self.VALID_WORKED_BY, jobs[0]['worked_by'])
            self.assertEqual(self.VALID_CONFIRMATION, jobs[0]['confirmation'])
            self.assertFalse(jobs[0]['has_paid'])
            self.assertEqual(self.yesterday, jobs[0]['start_date'])
            self.assertEqual(self.yesterday, jobs[0]['end_date'])
            # Assertions for job 2
            self.assertIn('Client 2', jobs[1]['client'])
            self.assertIn('Description 2', jobs[1]['description'])
            self.assertEqual(222.22, jobs[1]['amount_paid'])
            self.assertEqual(self.VALID_PAID_TO, jobs[1]['paid_to'])
            self.assertEqual(self.VALID_WORKED_BY, jobs[1]['worked_by'])
            self.assertEqual(self.VALID_CONFIRMATION, jobs[1]['confirmation'])
            self.assertTrue(jobs[1]['has_paid'])
            self.assertEqual(self.yesterday, jobs[1]['start_date'])
            self.assertEqual(self.today, jobs[1]['end_date'])
