# services/flask/project/tests/test_admin_api_users.py

import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestAdminApiUsers(BaseTestCase):
    """Tests for the /admin/users routes of the Admin Api Service."""

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/admin/users',
                data=json.dumps({
                    'username': 'Tyler',
                    'email': 'tjneisi@gmail.com',
                    'password': 'somePassword'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('User Tyler was added!', data['message'])
            self.assertIn('success', data['status'])
            self.assertEqual(len(data.keys()), 2)

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/admin/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        with self.client:
            response = self.client.post(
                '/admin/users',
                data=json.dumps({'email': 'tjneisi@gmail.com'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys_no_password(self):
        """
        Ensure error is thrown if the JSON object
        does not have a password key.
        """
        with self.client:
            response = self.client.post(
                '/admin/users',
                data=json.dumps(dict(
                    username='Tyler',
                    email='tjneisi@gmail.com')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post(
                '/admin/users',
                data=json.dumps({
                    'username': 'Tyler',
                    'email': 'tjneisi@gmail.com',
                    'password': 'somePassword'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/admin/users',
                data=json.dumps({
                    'username': 'Tyler',
                    'email': 'tjneisi@gmail.com',
                    'password': 'somePassword'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('Tyler', 'tjneisi@gmail.com', 'somePassword')
        with self.client:
            response = self.client.get(f'/admin/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Tyler', data['data']['username'])
            self.assertIn('tjneisi@gmail.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/admin/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/admin/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        add_user('Tyler', 'tjneisi@gmail.com', 'somePassword')
        add_user('Meghan', 'meghanunderwood8@gmail.com', 'someOtherPassword')
        with self.client:
            response = self.client.get('/admin/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('Tyler', data['data']['users'][0]['username'])
            self.assertIn(
                'tjneisi@gmail.com', data['data']['users'][0]['email'])
            self.assertIn('Meghan', data['data']['users'][1]['username'])
            self.assertIn('meghanunderwood8@gmail.com',
                          data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])


if __name__ == '__main__':
    unittest.main()
