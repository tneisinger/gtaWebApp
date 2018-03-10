# services/flask/project/tests/test_admin_api_expenses.py

import json
from datetime import date, timedelta

from project.tests.base import BaseTestCase
from project.admin.models import (OneTimeExpenseCategoryOption,
                                  OneTimeExpensePaidByOption)
from project.tests.utils import add_one_time_expense


class TestAdminApiJobs(BaseTestCase):
    """Tests for the /admin/expenses routes of the Admin Api Service."""

    # Get the dates for yesterday and today
    yesterday = (date.today() - timedelta(1)).isoformat()
    today = date.today().isoformat()

    # Get the first valid option from each enumeration
    VALID_PAID_BY = next(e.value for e in OneTimeExpensePaidByOption)
    VALID_CATEGORY = next(e.value for e in OneTimeExpenseCategoryOption)

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
                        'paid_by': self.VALID_PAID_BY,
                        'tax_deductible': True,
                        'category': self.VALID_CATEGORY
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
                        'paid_by': self.VALID_PAID_BY,
                        'tax_deductible': True,
                        'category': self.VALID_CATEGORY
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
                        'paid_by': self.VALID_PAID_BY,
                        'tax_deductible': True,
                        'category': self.VALID_CATEGORY
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
                        'paid_by': self.VALID_PAID_BY,
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
                    'paid_by': self.VALID_PAID_BY,
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
                        'category': self.VALID_CATEGORY
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
                    'category': self.VALID_CATEGORY
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

    def test_get_single_one_time_expense(self):
        """Ensure get single OneTimeExpense behaves correctly."""
        expense = add_one_time_expense(
                                        merchant='Test Merchant',
                                        description='Test Description',
                                        amount_spent=666.01,
                                        date=self.today,
                                        paid_by=self.VALID_PAID_BY,
                                        tax_deductible=True,
                                        category=self.VALID_CATEGORY
        )
        with self.client:
            url = f'/admin/one-time-expenses/{expense.id}'
            response = self.client.get(url)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Test Merchant', data['data']['merchant'])
            self.assertIn('Test Description', data['data']['description'])
            self.assertEqual(666.01, data['data']['amount_spent'])
            self.assertIn(self.today, data['data']['date'])
            self.assertEqual(self.VALID_PAID_BY, data['data']['paid_by'])
            self.assertTrue(data['data']['tax_deductible'])
            self.assertEqual(self.VALID_CATEGORY, data['data']['category'])
            self.assertIn('success', data['status'])

    def test_get_single_one_time_expense_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/admin/one-time-expenses/blurp')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Expense does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_single_one_time_expense_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/admin/one-time-expenses/9999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Expense does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_all_one_time_expenses(self):
        """Ensure get all one time expenses behaves correctly."""
        add_one_time_expense(
                merchant='Merchant 1',
                description='Description 1',
                amount_spent=111.11,
                date=self.yesterday,
                paid_by=self.VALID_PAID_BY,
                tax_deductible=False,
                category=self.VALID_CATEGORY
        )
        add_one_time_expense(
                merchant='Merchant 2',
                description='Description 2',
                amount_spent=222.22,
                date=self.today,
                paid_by=self.VALID_PAID_BY,
                tax_deductible=True,
                category=self.VALID_CATEGORY
        )
        with self.client:
            response = self.client.get('/admin/one-time-expenses')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(len(data['data']['one-time-expenses']), 2)
            expenses = data['data']['one-time-expenses']
            # Assertions for expense 1
            self.assertIn('Merchant 1', expenses[0]['merchant'])
            self.assertIn('Description 1', expenses[0]['description'])
            self.assertEqual(111.11, expenses[0]['amount_spent'])
            self.assertEqual(self.yesterday, expenses[0]['date'])
            self.assertEqual(self.VALID_PAID_BY, expenses[0]['paid_by'])
            self.assertFalse(expenses[0]['tax_deductible'])
            self.assertEqual(self.VALID_CATEGORY, expenses[0]['category'])
            # Assertions for expense 2
            self.assertIn('Merchant 2', expenses[1]['merchant'])
            self.assertIn('Description 2', expenses[1]['description'])
            self.assertEqual(222.22, expenses[1]['amount_spent'])
            self.assertEqual(self.today, expenses[1]['date'])
            self.assertEqual(self.VALID_PAID_BY, expenses[1]['paid_by'])
            self.assertTrue(expenses[1]['tax_deductible'])
            self.assertEqual(self.VALID_CATEGORY, expenses[1]['category'])
