# services/flask/project/tests/test_admin_auth.py

import json
import unittest

from flask import current_app

from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestAdminAuthRoutes(BaseTestCase):

    def test_user_registration(self):
        with self.client:
            response = self.client.post(
                '/admin/register',
                data=json.dumps({
                    'username': 'justatest',
                    'email': 'test@test.com',
                    'password': '123456',
                    'is_private_device': True
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        add_user('test', 'test@test.com', 'test')
        with self.client:
            response = self.client.post(
                '/admin/register',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'test@test.com',
                    'password': 'test',
                    'is_private_device': True
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That user already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_duplicate_username(self):
        add_user('test', 'test@test.com', 'test')
        with self.client:
            response = self.client.post(
                '/admin/register',
                data=json.dumps({
                    'username': 'test',
                    'email': 'test@test.com2',
                    'password': 'test',
                    'is_private_device': True
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That user already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/admin/register',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_username(self):
        with self.client:
            response = self.client.post(
                '/admin/register',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test',
                    'is_private_device': True
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_email(self):
        with self.client:
            response = self.client.post(
                '/admin/register',
                data=json.dumps({
                    'username': 'justatest',
                    'password': 'test',
                    'is_private_device': True
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_password(self):
        with self.client:
            response = self.client.post(
                '/admin/register',
                data=json.dumps({
                    'username': 'justatest',
                    'email': 'test@test.com',
                    'is_private_device': True
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_registered_user_login(self):
        with self.client:
            add_user('test', 'test@test.com', 'test')
            response = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test',
                    'is_private_device': True
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertTrue(data['user'])
            self.assertEqual(data['user']['username'], 'test')
            self.assertEqual(response.status_code, 200)

    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test',
                    'is_private_device': True
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(data['message'], 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_valid_logout(self):
        add_user('test', 'test@test.com', 'test')
        with self.client:
            # user login
            resp_login = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test',
                    'is_private_device': True
                }),
                content_type='application/json'
            )
            # valid token logout
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/admin/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout_expired_token(self):
        add_user('test', 'test@test.com', 'test')
        current_app.config['TOKEN_EXPIRE_SECONDS_LONG'] = -1
        with self.client:
            resp_login = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test',
                    'is_private_device': True
                }),
                content_type='application/json'
            )
            # invalid token logout
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/admin/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout(self):
        with self.client:
            response = self.client.get(
                '/admin/logout',
                headers={'Authorization': 'Bearer invalid'})
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_user_status(self):
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test',
                    'is_private_device': True
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/admin/status',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == 'test')
            self.assertTrue(data['data']['email'] == 'test@test.com')
            self.assertEqual(response.status_code, 200)

    def test_invalid_status(self):
        with self.client:
            response = self.client.get(
                '/admin/status',
                headers={'Authorization': 'Bearer invalid'})
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_status_expired_token(self):
        add_user('test', 'test@test.com', 'test')
        current_app.config['TOKEN_EXPIRE_SECONDS_LONG'] = -1
        current_app.config['TOKEN_EXPIRE_DAYS_LONG'] = -1
        with self.client:
            resp_login = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test',
                    'is_private_device': True
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/admin/status',
                headers={'Authorization': f'Bearer {token}'})
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            print(data['message'])
            self.assertTrue(
                data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_status_private_device_uses_long_token_expire(self):
        add_user('test', 'test@test.com', 'test')

        # The LONG TOKEN_EXPIRE constants should be used when the user logs in
        # with is_private_device set to true, so if we set the SHORT constants
        # to an invalid value, we should still get a good status response.
        current_app.config['TOKEN_EXPIRE_SECONDS_SHORT'] = -1
        current_app.config['TOKEN_EXPIRE_DAYS_SHORT'] = -1
        with self.client:
            resp_login = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test',
                    'is_private_device': True
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/admin/status',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == 'test')
            self.assertTrue(data['data']['email'] == 'test@test.com')
            self.assertEqual(response.status_code, 200)

    def test_status_public_device_uses_short_token_expire(self):
        add_user('test', 'test@test.com', 'test')

        # The SHORT TOKEN_EXPIRE constants should be used when the user logs in
        # with is_private_device set to false, so if we set the LONG constants
        # to an invalid value, we should still get a good status response.
        current_app.config['TOKEN_EXPIRE_SECONDS_LONG'] = -1
        current_app.config['TOKEN_EXPIRE_DAYS_LONG'] = -1
        with self.client:
            resp_login = self.client.post(
                '/admin/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'test',
                    'is_private_device': False
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/admin/status',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == 'test')
            self.assertTrue(data['data']['email'] == 'test@test.com')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
