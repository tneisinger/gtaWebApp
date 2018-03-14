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
        'client': 'Test client1',
        'description': 'Test description1',
        'amount_paid': 666.01,
        'paid_to': next(p.value for p in Job.PaidTo),
        'worked_by': next(w.value for w in Job.WorkedBy),
        'confirmation': next(c.value for c in Job.Confirmation),
        'has_paid': False,
        'start_date': (FIRST_DAY + timedelta(5)).isoformat()
    }

    # Create a dictionary for a valid one time expense
    VALID_EXPENSE_DICT1 = {
        'merchant': 'Test Merchant',
        'description': 'Test Description',
        'amount_spent': 666.01,
        'date': FIRST_DAY.isoformat(),
        'paid_by': next(e.value for e in OneTimeExpense.PaidBy),
        'tax_deductible': True,
        'category': next(e.value for e in OneTimeExpense.Category),
    }

    FAKE_TOKEN = ('wnK6eXAiOiJK21QiLfJhbqciOiJIUzI1NiJ9.eyJleHAiOj' +
                  'E1MjA5ODMyNzYsImlhdCIDMTUyMDk4MzI3Mywic3ViIjoxfQ.k' +
                  'YQbY1Fj8pB4oK2nHmRuPWp3bDtHFwa000000000000')

    def test_get_calendar_events(self):
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
                '/admin/auth/login',
                data=json.dumps({
                    'email': self.VALID_USER_DICT1['email'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(resp_login.data.decode())['auth_token']

            # request the calendar data
            request_data = {
                     'start_date': self.FIRST_DAY.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_calendar_events', **request_data),
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())

            # Assert that everything went well
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')

            # Before comparing the returned job with the job we
            # added, we must pop the id key from the returned job,
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

    def test_get_calendar_events_not_signed_in(self):
        """
        Test attempting to get jobs and one-time-expenses (calendar events)
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

            # request the calendar data
            request_data = {
                     'start_date': self.FIRST_DAY.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_calendar_events', **request_data)
            )
            data = json.loads(response.data.decode())

            # Assert that it failed
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Provide a valid auth token.')

    def test_get_calendar_events_fake_auth_token(self):
        """
        Test attempting to get calendar events using a fake auth token
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
                '/admin/auth/login',
                data=json.dumps({
                    'email': self.VALID_USER_DICT1['email'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # request the calendar data
            request_data = {
                     'start_date': self.FIRST_DAY.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_calendar_events', **request_data),
                headers={'Authorization': f'Bearer {self.FAKE_TOKEN}'}
            )
            data = json.loads(response.data.decode())

            # Assert that it failed
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Provide a valid auth token.')

    def test_get_calendar_events_empty_auth_header(self):
        """
        Test attempting to get calendar events with an empty Authorization
        header
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
                '/admin/auth/login',
                data=json.dumps({
                    'email': self.VALID_USER_DICT1['email'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # request the calendar data
            request_data = {
                     'start_date': self.FIRST_DAY.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_calendar_events', **request_data),
                headers={'Authorization': ''}
            )
            data = json.loads(response.data.decode())

            # Assert that it failed
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Provide a valid auth token.')

    def test_get_calendar_events_user_not_admin(self):
        """
        Test attempting to get calendar events with an empty Authorization
        header
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
                '/admin/auth/login',
                data=json.dumps({
                    'email': self.VALID_USER_DICT1['email'],
                    'password': self.VALID_USER_DICT1['password']
                }),
                content_type='application/json'
            )

            # get the user's auth token
            token = json.loads(resp_login.data.decode())['auth_token']

            # request the calendar data
            request_data = {
                     'start_date': self.FIRST_DAY.isoformat(),
                     'end_date': self.LAST_DAY.isoformat()
            }
            response = self.client.get(
                url_for('admin.get_calendar_events', **request_data),
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())

            # Assert that it failed
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'User must be admin.')


if __name__ == "__main__":
    unittest.main()
