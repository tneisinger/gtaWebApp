# services/flask/project/tests/test_admin_api_expenses.py

import json
from datetime import date, timedelta

from project.tests.base import BaseTestCase
from project.admin.models import (OneTimeExpenseCategoryOption,
                                  OneTimeExpensePaidByOption,
                                  RecurringExpense)
from project.tests.utils import add_one_time_expense


class TestAdminApiJobs(BaseTestCase):
    """Tests for the /admin/expenses routes of the Admin Api Service."""

    # Get the dates for yesterday and today
    yesterday = (date.today() - timedelta(1)).isoformat()
    today = date.today().isoformat()

    VALID_ONE_TIME_EXPENSE_DICT = {
        'merchant': 'Test Merchant',
        'description': 'Test Description',
        'amount_spent': 666.01,
        'date': today,
        'paid_by': next(e.value for e in OneTimeExpensePaidByOption),
        'tax_deductible': True,
        'category': next(e.value for e in OneTimeExpenseCategoryOption),
    }

    VALID_RECURRING_EXPENSE_DICT = {
        'merchant': 'Test Merchant',
        'description': 'Test Description',
        'amount': 666.01,
        'is_deductible': True,
        'category': next(e.value for e in RecurringExpense.CategoryOption),
        'recurrence': next(e.value for e in RecurringExpense.RecurrenceOption),
        'paid_by': next(e.value for e in RecurringExpense.PaidByOption),
        'start_date': today
    }

    # ======================
    # ONE TIME EXPENSE TESTS
    # ======================

    def test_add_one_time_expense(self):
        """Ensure a new one time expense can be added to the database."""
        with self.client:
            response = self.client.post(
                    '/admin/one-time-expenses',
                    data=json.dumps(self.VALID_ONE_TIME_EXPENSE_DICT),
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
        invalid_expense_dict = self.VALID_ONE_TIME_EXPENSE_DICT.copy()
        invalid_expense_dict.pop('merchant')
        with self.client:
            response = self.client.post(
                '/admin/one-time-expenses',
                data=json.dumps(invalid_expense_dict),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_one_time_expense_amount_spent_not_a_number(self):
        """Ensure error thrown if amount_spent is non-numeric"""
        invalid_expense_dict = self.VALID_ONE_TIME_EXPENSE_DICT.copy()
        invalid_expense_dict['amount_spent'] = 'INVALID NON-NUMERIC!'
        with self.client:
            response = self.client.post(
                '/admin/one-time-expenses',
                data=json.dumps(invalid_expense_dict),
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
        valid_expense_dict = self.VALID_ONE_TIME_EXPENSE_DICT.copy()
        for valid_category_val in [t.value
                                   for t in OneTimeExpenseCategoryOption]:
            valid_expense_dict['category'] = valid_category_val
            with self.client:
                response = self.client.post(
                    '/admin/one-time-expenses',
                    data=json.dumps(valid_expense_dict),
                    content_type='application/json',
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)
                self.assertIn('Test Merchant expense was added!',
                              data['message'])
                self.assertIn('success', data['status'])

    def test_add_one_time_expense_with_invalid_category_val(self):
        """
        Ensure that a one time expense with an invalid category value
        cannot be added to the database.
        """
        invalid_expense_dict = self.VALID_ONE_TIME_EXPENSE_DICT.copy()
        invalid_expense_dict['category'] = 'INVALID!!!'
        with self.client:
            response = self.client.post(
                '/admin/one-time-expenses',
                data=json.dumps(invalid_expense_dict),
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
        valid_expense_dict = self.VALID_ONE_TIME_EXPENSE_DICT.copy()
        for valid_paid_by_val in [t.value
                                  for t in OneTimeExpensePaidByOption]:
            valid_expense_dict['paid_by'] = valid_paid_by_val
            with self.client:
                response = self.client.post(
                    '/admin/one-time-expenses',
                    data=json.dumps(valid_expense_dict),
                    content_type='application/json',
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)
                self.assertIn('Test Merchant expense was added!',
                              data['message'])
                self.assertIn('success', data['status'])

    def test_add_one_time_expense_with_invalid_paid_by_val(self):
        """
        Ensure that a one time expense with an invalid paid_by value
        cannot be added to the database.
        """
        invalid_expense_dict = self.VALID_ONE_TIME_EXPENSE_DICT.copy()
        invalid_expense_dict['paid_by'] = 'INVALID!!!'
        with self.client:
            response = self.client.post(
                '/admin/one-time-expenses',
                data=json.dumps(invalid_expense_dict),
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
        expense = add_one_time_expense(**self.VALID_ONE_TIME_EXPENSE_DICT)
        with self.client:
            url = f'/admin/one-time-expenses/{expense.id}'
            response = self.client.get(url)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(1, data['data'].pop('id'))
            self.assertEqual(self.VALID_ONE_TIME_EXPENSE_DICT, data['data'])

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

        # Create the first expense
        valid_expense_dict1 = self.VALID_ONE_TIME_EXPENSE_DICT.copy()
        valid_expense_dict1['merchant'] = 'Merchant 1'
        valid_expense_dict1['description'] = 'Description 1'
        valid_expense_dict1['amount_spent'] = 111.11
        valid_expense_dict1['tax_deductible'] = False
        valid_expense_dict1['date'] = self.yesterday

        # Create the second expense
        valid_expense_dict2 = self.VALID_ONE_TIME_EXPENSE_DICT.copy()
        valid_expense_dict2['merchant'] = 'Merchant 2'
        valid_expense_dict2['description'] = 'Description 2'
        valid_expense_dict2['amount_spent'] = 222.22

        # Add them to the db
        add_one_time_expense(**valid_expense_dict1)
        add_one_time_expense(**valid_expense_dict2)

        with self.client:
            response = self.client.get('/admin/one-time-expenses')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(len(data['data']['one-time-expenses']), 2)
            expenses = data['data']['one-time-expenses']
            # Assertions for expense 1
            self.assertEqual(1, expenses[0].pop('id'))
            self.assertEqual(valid_expense_dict1, expenses[0])
            # Assertions for expense 2
            self.assertEqual(2, expenses[1].pop('id'))
            self.assertEqual(valid_expense_dict2, expenses[1])

    # =======================
    # RECURRING EXPENSE TESTS
    # =======================

    def test_add_recurring_expense(self):
        """Ensure a new recurring expense can be added to the database."""
        with self.client:
            response = self.client.post(
                    '/admin/recurring-expenses',
                    data=json.dumps(self.VALID_RECURRING_EXPENSE_DICT),
                    content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            msg = 'Test Merchant recurring expense was added!'
            self.assertIn(msg, data['message'])
            self.assertIn('success', data['status'])

    def test_add_recurring_expense_empty_json(self):
        """Ensure that an error is thrown if json is empty"""
        with self.client:
            response = self.client.post(
                    '/admin/recurring-expenses',
                    data=json.dumps({}),
                    content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_recurring_expense_missing_key(self):
        """Ensure that an error is thrown if json is missing a key"""
        invalid_expense_dict = self.VALID_RECURRING_EXPENSE_DICT.copy()
        invalid_expense_dict.pop('merchant')
        with self.client:
            response = self.client.post(
                    '/admin/recurring-expenses',
                    data=json.dumps(invalid_expense_dict),
                    content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_recurring_expense_invalid_recurrence_value(self):
        """Ensure error is thrown if an invalid recurrence value given"""
        invalid_expense_dict = self.VALID_RECURRING_EXPENSE_DICT.copy()
        invalid_expense_dict['recurrence'] = 'INVALID!!!'
        with self.client:
            response = self.client.post(
                    '/admin/recurring-expenses',
                    data=json.dumps(invalid_expense_dict),
                    content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            err_msg = ("Invalid 'recurrence' value. " +
                       "The valid values for 'recurrence' are: " +
                       ', '.join([f"'{t.value}'"
                                  for t in RecurringExpense.RecurrenceOption]))
            self.assertEqual(err_msg, data['message'])
            self.assertIn('fail', data['status'])

    def test_add_recurring_expense_invalid_paid_by_value(self):
        """Ensure error is thrown if an invalid paid_by value given"""
        invalid_expense_dict = self.VALID_RECURRING_EXPENSE_DICT.copy()
        invalid_expense_dict['paid_by'] = 'INVALID!!!'
        with self.client:
            response = self.client.post(
                    '/admin/recurring-expenses',
                    data=json.dumps(invalid_expense_dict),
                    content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            err_msg = ("Invalid 'paid_by' value. " +
                       "The valid values for 'paid_by' are: " +
                       ', '.join([f"'{t.value}'"
                                  for t in RecurringExpense.PaidByOption]))
            self.assertEqual(err_msg, data['message'])
            self.assertIn('fail', data['status'])

    def test_add_recurring_expense_invalid_category_value(self):
        """Ensure error is thrown if an invalid category value given"""
        invalid_expense_dict = self.VALID_RECURRING_EXPENSE_DICT.copy()
        invalid_expense_dict['category'] = 'INVALID!!!'
        with self.client:
            response = self.client.post(
                    '/admin/recurring-expenses',
                    data=json.dumps(invalid_expense_dict),
                    content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            err_msg = ("Invalid 'category' value. " +
                       "The valid values for 'category' are: " +
                       ', '.join([f"'{t.value}'"
                                  for t in RecurringExpense.CategoryOption]))
            self.assertEqual(err_msg, data['message'])
            self.assertIn('fail', data['status'])
