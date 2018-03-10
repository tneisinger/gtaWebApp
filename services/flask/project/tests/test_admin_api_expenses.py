# services/flask/project/tests/test_admin_api_expenses.py

import json
from datetime import date

from project.tests.base import BaseTestCase
from project.admin.models import (OneTimeExpenseCategoryOption,
                                  OneTimeExpensePaidByOption)


class TestAdminApiJobs(BaseTestCase):
    """Tests for the /admin/expenses routes of the Admin Api Service."""

    today = date.today().isoformat()

    def test_add_one_time_expense(self):
        """Ensure a new one time expense can be added to the database."""
        with self.client:
            response = self.client.post(
                    '/admin/one-time-expenses',
                    data=json.dumps({
                        'merchant': 'Test Merchant',
                        'description': 'Test Description',
                        'amount_spent': 666.01,
                        'date': self.today,
                        'paid_by': 'Tyler',
                        'tax_deductible': True,
                        'category': 'Business Equipment'
                    }),
                    content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Test Merchant expense was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_one_time_expense_empty_json(self):
        """Ensure an error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/admin/one-time-expenses',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_one_time_expense_invalid_json_missing_key(self):
        """Ensure error thrown if JSON object does not have a merchant key."""
        with self.client:
            response = self.client.post(
                '/admin/one-time-expenses',
                data=json.dumps({
                        'description': 'Test Description',
                        'amount_spent': 666.01,
                        'date': self.today,
                        'paid_by': 'Tyler',
                        'tax_deductible': True,
                        'category': 'Business Equipment'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_one_time_expense_amount_spent_not_a_number(self):
        """Ensure error thrown if amount_spent is non-numeric"""
        with self.client:
            response = self.client.post(
                '/admin/one-time-expenses',
                data=json.dumps({
                        'merchant': 'Test Merchant',
                        'description': 'Test Description',
                        'amount_spent': 'INVALID NON-NUMERIC VALUE!',
                        'date': self.today,
                        'paid_by': 'Tyler',
                        'tax_deductible': True,
                        'category': 'Business Equipment'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("'amount_spent' must be a number.", data['message'])
            self.assertIn('fail', data['status'])

    def test_add_one_time_expenses_with_valid_category_vals(self):
        """
        Ensure one time expenses with valid category values can be
        added to the db
        """
        for valid_category_val in [t.value
                                   for t in OneTimeExpenseCategoryOption]:
            with self.client:
                response = self.client.post(
                    '/admin/one-time-expenses',
                    data=json.dumps({
                        'merchant': valid_category_val,
                        'description': 'Test Description',
                        'amount_spent': 666.01,
                        'date': self.today,
                        'paid_by': 'Tyler',
                        'tax_deductible': True,
                        'category': valid_category_val
                    }),
                    content_type='application/json',
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)
                self.assertIn(valid_category_val + ' expense was added!',
                              data['message'])
                self.assertIn('success', data['status'])

    def test_add_one_time_expense_with_invalid_category_val(self):
        """
        Ensure that a one time expense with an invalid category value
        cannot be added to the database.
        """
        with self.client:
            response = self.client.post(
                '/admin/one-time-expenses',
                data=json.dumps({
                    'merchant': 'Test Client',
                    'description': 'Test Description',
                    'amount_spent': 666.01,
                    'date': self.today,
                    'paid_by': 'Tyler',
                    'tax_deductible': True,
                    'category': 'INVALID!!!'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            err_msg = ("Invalid 'category' value. " +
                       "The valid values for 'category' are: " +
                       ', '.join([f"'{t.value}'"
                                  for t in OneTimeExpenseCategoryOption]))
            self.assertEqual(err_msg, data['message'])
            self.assertIn('fail', data['status'])

    def test_add_one_time_expenses_with_valid_paid_by_vals(self):
        """
        Ensure one time expenses with valid paid_by values can be
        added to the db
        """
        for valid_paid_by_val in [t.value
                                  for t in OneTimeExpensePaidByOption]:
            with self.client:
                response = self.client.post(
                    '/admin/one-time-expenses',
                    data=json.dumps({
                        'merchant': valid_paid_by_val,
                        'description': 'Test Description',
                        'amount_spent': 666.01,
                        'date': self.today,
                        'paid_by': valid_paid_by_val,
                        'tax_deductible': True,
                        'category': 'Business Equipment'
                    }),
                    content_type='application/json',
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)
                self.assertIn(valid_paid_by_val + ' expense was added!',
                              data['message'])
                self.assertIn('success', data['status'])

    def test_add_one_time_expense_with_invalid_paid_by_val(self):
        """
        Ensure that a one time expense with an invalid paid_by value
        cannot be added to the database.
        """
        with self.client:
            response = self.client.post(
                '/admin/one-time-expenses',
                data=json.dumps({
                    'merchant': 'Test Client',
                    'description': 'Test Description',
                    'amount_spent': 666.01,
                    'date': self.today,
                    'paid_by': 'INVALID!!!',
                    'tax_deductible': True,
                    'category': 'Business Equipment'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            err_msg = ("Invalid 'paid_by' value. " +
                       "The valid values for 'paid_by' are: " +
                       ', '.join([f"'{t.value}'"
                                  for t in OneTimeExpensePaidByOption]))
            self.assertEqual(err_msg, data['message'])
            self.assertIn('fail', data['status'])
