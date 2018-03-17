import json
import unittest
from datetime import date, timedelta
from calendar import monthrange

from flask import url_for

from project.tests.base import BaseTestCase
from project.admin.models import Job, OneTimeExpense
from project.tests.utils import (add_user, make_user_admin, add_job,
                                 add_one_time_expense)


class TestAdminCalendarRoutes(BaseTestCase):

    # Get the dates for the first and last days of the month
    today = date.today()
    num_month_days = monthrange(today.year, today.month)[1]
    FIRST_DAY = today.replace(day=1)
    LAST_DAY = today.replace(day=num_month_days)

    # Create a dictionary for a valid user
    VALID_USER_DICT1 = {
        'username': 'test user 1',
        'email': 'user1@email.com',
        'password': 'somePassword'
    }

    # Create a dictionary for a valid job
    VALID_JOB_DICT1 = {
        'client': 'Job Client 1',
        'description': 'Job Description 1',
        'amount_paid': 111.11,
        'paid_to': next(p.value for p in Job.PaidTo),
        'worked_by': next(w.value for w in Job.WorkedBy),
        'confirmation': next(c.value for c in Job.Confirmation),
        'has_paid': False,
        'start_date': (FIRST_DAY + timedelta(5)).isoformat()
    }

    # Another valid job
    VALID_JOB_DICT2 = {
        'client': 'Job Client 2',
        'description': 'Job Description 2',
        'amount_paid': 222.22,
        'paid_to': next(p.value for p in Job.PaidTo),
        'worked_by': next(w.value for w in Job.WorkedBy),
        'confirmation': next(c.value for c in Job.Confirmation),
        'has_paid': True,
        'start_date': (FIRST_DAY + timedelta(25)).isoformat()
    }

    # Create a dictionary for a valid one time expense
    VALID_EXPENSE_DICT1 = {
        'merchant': 'Expense Merchant 1',
        'description': 'Expense Description 1',
        'amount_spent': 111.01,
        'date': (FIRST_DAY + timedelta(3)).isoformat(),
        'paid_by': next(e.value for e in OneTimeExpense.PaidBy),
        'tax_deductible': True,
        'category': next(e.value for e in OneTimeExpense.Category),
    }

    VALID_EXPENSE_DICT2 = {
        'merchant': 'Expense Merchant 2',
        'description': 'Expense Description 2',
        'amount_spent': 222.02,
        'date': (FIRST_DAY + timedelta(15)).isoformat(),
        'paid_by': next(e.value for e in OneTimeExpense.PaidBy),
        'tax_deductible': False,
        'category': next(e.value for e in OneTimeExpense.Category),
    }

    FAKE_TOKEN = ('wnK6eXAiOiJK21QiLfJhbqciOiJIUzI1NiJ9.eyJleHAiOj' +
                  'E1MjA5ODMyNzYsImlhdCIDMTUyMDk4MzI3Mywic3ViIjoxfQ.k' +
                  'YQbY1Fj8pB4oK2nHmRuPWp3bDtHFwa000000000000')

    def test_get_events(self):
        """
        Test getting jobs and one-time-expenses that fall between the dates
        provided in a query string. (User must be signed in and user must be
        admin to get a successful response.)
        """
        # Add a user to the db
        user = add_user(**self.VALID_USER_DICT1)

        # Set the user's is_admin database column to True
        make_user_admin(user)

        # Add a job and an expense to the database
        add_job(**self.VALID_JOB_DICT1)
        add_one_time_expense(**self.VALID_EXPENSE_DICT1)

        with self.client:

            # login as user
            resp_login = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'email': self.VALID_USER_DICT1['email'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(resp_login.data.decode())['auth_token']

            # request the events that occurred between start_date and end_date
            request_data = {
                     'start_date': self.FIRST_DAY.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_events', **request_data),
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())

            # Assert that everything went well
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')

            # Before comparing the returned job with the job we
            # added, we must pop the id key from the returned job,
            # While, we're at it, let's check that it is what we expect.
            self.assertEqual(1, data['data']['jobs'][0].pop('id'))

            # We also need to pop off the end_date key, since we
            # didn't provide one.  When we create a job without
            # specifying an end_date, the end_date column gets
            # populated with the start_date value.  So pop the
            # end_date value and check that it matches the
            # start_date value that we sent in self.VALID_JOB_DICT1
            self.assertEqual(self.VALID_JOB_DICT1['start_date'],
                             data['data']['jobs'][0].pop('end_date'))

            # Now that we have removed the id and the end_date,
            # the sent job and the returned job should be identical.
            self.assertEqual(self.VALID_JOB_DICT1, data['data']['jobs'][0])

            # Similar to above, we must pop the id key from the returned
            # expense before we can compare it to the sent expense.
            self.assertEqual(1, data['data']['expenses'][0].pop('id'))
            self.assertEqual(self.VALID_EXPENSE_DICT1,
                             data['data']['expenses'][0])

            # Check that the user data is included and correct
            self.assertEqual(data['data']['user']['username'],
                             self.VALID_USER_DICT1['username'])
            self.assertEqual(data['data']['user']['email'],
                             self.VALID_USER_DICT1['email'])
            self.assertEqual(data['data']['user']['id'], 1)

    def test_get_events_not_signed_in(self):
        """
        Test attempting to get jobs and one-time-expenses (events)
        without being signed in.
        """
        # Add a user to the db
        user = add_user(**self.VALID_USER_DICT1)

        # Set the user's is_admin database column to True
        make_user_admin(user)

        # Add a job and an expense to the database
        add_job(**self.VALID_JOB_DICT1)
        add_one_time_expense(**self.VALID_EXPENSE_DICT1)

        with self.client:

            # request the events
            request_data = {
                     'start_date': self.FIRST_DAY.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_events', **request_data)
            )
            data = json.loads(response.data.decode())

            # Assert that it failed
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Provide a valid auth token.')

    def test_get_events_fake_auth_token(self):
        """
        Test attempting to get events using a fake auth token
        """
        # Add a user to the db
        user = add_user(**self.VALID_USER_DICT1)

        # Set the user's is_admin database column to True
        make_user_admin(user)

        # Add a job and an expense to the database
        add_job(**self.VALID_JOB_DICT1)
        add_one_time_expense(**self.VALID_EXPENSE_DICT1)

        with self.client:

            # login as user
            self.client.post(
                '/admin/login',
                data=json.dumps({
                    'email': self.VALID_USER_DICT1['email'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # request the events
            request_data = {
                     'start_date': self.FIRST_DAY.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_events', **request_data),
                headers={'Authorization': f'Bearer {self.FAKE_TOKEN}'}
            )
            data = json.loads(response.data.decode())

            # Assert that it failed
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Provide a valid auth token.')

    def test_get_events_empty_auth_header(self):
        """
        Test attempting to get events with an empty Authorization header
        """
        # Add a user to the db
        user = add_user(**self.VALID_USER_DICT1)

        # Set the user's is_admin database column to True
        make_user_admin(user)

        # Add a job and an expense to the database
        add_job(**self.VALID_JOB_DICT1)
        add_one_time_expense(**self.VALID_EXPENSE_DICT1)

        with self.client:

            # login as user
            self.client.post(
                '/admin/login',
                data=json.dumps({
                    'email': self.VALID_USER_DICT1['email'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # request the events
            request_data = {
                     'start_date': self.FIRST_DAY.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_events', **request_data),
                headers={'Authorization': ''}
            )
            data = json.loads(response.data.decode())

            # Assert that it failed
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Provide a valid auth token.')

    def test_get_events_no_auth_header(self):
        """
        Test attempting to get events without an auth header
        """
        # Add a user to the db
        user = add_user(**self.VALID_USER_DICT1)

        # Set the user's is_admin database column to True
        make_user_admin(user)

        # Add a job and an expense to the database
        add_job(**self.VALID_JOB_DICT1)
        add_one_time_expense(**self.VALID_EXPENSE_DICT1)

        with self.client:

            # login as user
            self.client.post(
                '/admin/login',
                data=json.dumps({
                    'email': self.VALID_USER_DICT1['email'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # request the events
            request_data = {
                     'start_date': self.FIRST_DAY.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_events', **request_data)
            )
            data = json.loads(response.data.decode())

            # Assert that it failed
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Provide a valid auth token.')

    def test_get_events_user_not_admin(self):
        """
        Test attempting to get events when the user is not an admin
        """
        # Add a user to the db
        add_user(**self.VALID_USER_DICT1)

        # Leave the user's is_admin database column set to False

        # Add a job and an expense to the database
        add_job(**self.VALID_JOB_DICT1)
        add_one_time_expense(**self.VALID_EXPENSE_DICT1)

        with self.client:

            # login as user
            resp_login = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'email': self.VALID_USER_DICT1['email'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(resp_login.data.decode())['auth_token']

            # request the events
            request_data = {
                     'start_date': self.FIRST_DAY.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_events', **request_data),
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())

            # Assert that it failed
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'User must be admin.')

    def test_get_events_no_events_in_range(self):
        """
        Test getting jobs and one-time-expenses when there are no events in the
        date range.  The response should include an empty jobs list, an empty
        expenses list, and the user data.
        """
        # Add a user to the db
        user = add_user(**self.VALID_USER_DICT1)

        # Set the user's is_admin database column to True
        make_user_admin(user)

        # Add a job and an expense to the database
        add_job(**self.VALID_JOB_DICT1)  # start_date and end_date is the 6th
        add_one_time_expense(**self.VALID_EXPENSE_DICT1)  # date is the 4th

        with self.client:

            # login as user
            resp_login = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'email': self.VALID_USER_DICT1['email'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(resp_login.data.decode())['auth_token']

            # Define a start date that is later than both the job and the
            # expense that we added above.
            start_date = self.FIRST_DAY + timedelta(10)

            # request the events
            request_data = {
                     'start_date': start_date.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_events', **request_data),
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())

            # Assert that everything went well
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')

            # There should be an empty jobs list in the data
            self.assertEqual(data['data']['jobs'], [])

            # There should be an empty expenses list in the data
            self.assertEqual(data['data']['expenses'], [])

            # Check that the user data is included and correct
            self.assertEqual(data['data']['user']['username'],
                             self.VALID_USER_DICT1['username'])
            self.assertEqual(data['data']['user']['email'],
                             self.VALID_USER_DICT1['email'])
            self.assertEqual(data['data']['user']['id'], 1)

    def test_get_events_some_events_out_of_range(self):
        """
        Test getting jobs and one-time-expenses when there are some events in
        the database that are not within the date range.  Events outside the
        date range should not be returned.
        """
        # Add a user to the db
        user = add_user(**self.VALID_USER_DICT1)

        # Set the user's is_admin database column to True
        make_user_admin(user)

        # Add a job and an expense to the database
        add_job(**self.VALID_JOB_DICT1)  # start_date and end_date is the 6th
        add_job(**self.VALID_JOB_DICT2)  # start_date and end_date is the 26th
        add_one_time_expense(**self.VALID_EXPENSE_DICT1)  # date is the 4th
        add_one_time_expense(**self.VALID_EXPENSE_DICT2)  # date is the 16th

        with self.client:

            # login as user
            resp_login = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'email': self.VALID_USER_DICT1['email'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(resp_login.data.decode())['auth_token']

            # Define a start date that is later than the first job and the
            # first expense that we added to the db above.
            start_date = self.FIRST_DAY + timedelta(10)

            # request the events
            request_data = {
                     'start_date': start_date.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_events', **request_data),
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())

            # Assert that everything went well
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')

            # There should be a jobs list in the data of length 1
            self.assertEqual(len(data['data']['jobs']), 1)

            # There should be an expenses list in the data of length 1
            self.assertEqual(len(data['data']['expenses']), 1)

            # Before comparing the returned job with the job we
            # added, we must pop the id key from the returned job,
            # While, we're at it, let's check that it is what we expect.
            self.assertEqual(2, data['data']['jobs'][0].pop('id'))

            # We also need to pop off the end_date key, since we
            # didn't provide one.  When we create a job without
            # specifying an end_date, the end_date column gets
            # populated with the start_date value.  So pop the
            # end_date value and check that it matches the
            # start_date value that we sent in self.VALID_JOB_DICT1
            self.assertEqual(self.VALID_JOB_DICT2['start_date'],
                             data['data']['jobs'][0].pop('end_date'))

            # Now that we have removed the id and the end_date,
            # the sent job and the returned job should be identical.
            self.assertEqual(self.VALID_JOB_DICT2, data['data']['jobs'][0])

            # Similar to above, we must pop the id key from the returned
            # expense before we can compare it to the sent expense.
            self.assertEqual(2, data['data']['expenses'][0].pop('id'))
            self.assertEqual(self.VALID_EXPENSE_DICT2,
                             data['data']['expenses'][0])

            # Check that the user data is included and correct
            self.assertEqual(data['data']['user']['username'],
                             self.VALID_USER_DICT1['username'])
            self.assertEqual(data['data']['user']['email'],
                             self.VALID_USER_DICT1['email'])
            self.assertEqual(data['data']['user']['id'], 1)

    def test_get_events_job_spans_start_of_date_range(self):
        """
        Test getting jobs and one-time-expenses when a job spands the start of
        the date range.
        """
        # Make a copy of the first job dict
        valid_job_dict1 = self.VALID_JOB_DICT1.copy()

        # Modify the dates of the first job dict so that it spans over the
        # first day of the month
        valid_job_dict1['start_date'] = (self.FIRST_DAY -
                                         timedelta(2)).isoformat()
        valid_job_dict1['end_date'] = (self.FIRST_DAY +
                                       timedelta(2)).isoformat()

        # Add a user to the db
        user = add_user(**self.VALID_USER_DICT1)

        # Set the user's is_admin database column to True
        make_user_admin(user)

        # Add the job events to the db
        add_job(**valid_job_dict1)
        add_job(**self.VALID_JOB_DICT2)

        with self.client:

            # login as user
            resp_login = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'email': self.VALID_USER_DICT1['email'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(resp_login.data.decode())['auth_token']

            # request the events
            request_data = {
                     'start_date': self.FIRST_DAY.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_events', **request_data),
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())

            # Assert that everything went well
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')

            # There should be a jobs list in the data of length 2
            self.assertEqual(len(data['data']['jobs']), 2)

    def test_get_events_job_spans_end_of_date_range(self):
        """
        Test getting jobs and one-time-expenses when a job spands the end of
        the date range.
        """
        # Make a copy of the second job dict
        valid_job_dict2 = self.VALID_JOB_DICT2.copy()

        # Modify the dates of the second job dict so that it spans over the
        # last day of the month
        valid_job_dict2['start_date'] = (self.LAST_DAY -
                                         timedelta(2)).isoformat()
        valid_job_dict2['end_date'] = (self.LAST_DAY +
                                       timedelta(2)).isoformat()

        # Add a user to the db
        user = add_user(**self.VALID_USER_DICT1)

        # Set the user's is_admin database column to True
        make_user_admin(user)

        # Add the jobs to the db
        add_job(**self.VALID_JOB_DICT1)
        add_job(**valid_job_dict2)

        with self.client:

            # login as user
            resp_login = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'email': self.VALID_USER_DICT1['email'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(resp_login.data.decode())['auth_token']

            # request the events
            request_data = {
                     'start_date': self.FIRST_DAY.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_events', **request_data),
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())

            # Assert that everything went well
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')

            # There should be a jobs list in the data of length 2
            self.assertEqual(len(data['data']['jobs']), 2)


if __name__ == "__main__":
    unittest.main()
