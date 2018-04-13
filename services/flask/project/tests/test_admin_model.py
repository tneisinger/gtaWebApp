# services/flask/project/tests/test_admin_model.py

import unittest
import datetime

from sqlalchemy.exc import IntegrityError

from project import db
from project.admin.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = add_user('justatest', 'test@test.com', 'somePassword')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')

    def test_add_user_duplicate_username(self):
        add_user('justatest', 'test@test.com', 'somePassword')
        duplicate_user = User(
            username='justatest',
            email='test@test2.com',
            password='somePassword'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user('justatest', 'test@test.com', 'somePassword')
        duplicate_user = User(
            username='justanothertest',
            email='test@test.com',
            password='somePassword'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user('justatest', 'test@test.com', 'somePassword')
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user_one = add_user('justatest', 'test@test.com', 'somepassword')
        user_two = add_user('justatest2', 'test@test2.com', 'somepassword')
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token_private_device(self):
        user = add_user('justatest', 'test@test.com', 'test')
        token, exp = user.encode_auth_token(user.id, is_private_device=True)
        self.assertTrue(isinstance(token, bytes))
        self.assertTrue(isinstance(exp, datetime.datetime))

    def test_encode_auth_token_public_device(self):
        user = add_user('justatest', 'test@test.com', 'test')
        token, exp = user.encode_auth_token(user.id, is_private_device=False)
        self.assertTrue(isinstance(token, bytes))
        self.assertTrue(isinstance(exp, datetime.datetime))

    def test_decode_auth_token(self):
        user = add_user('justatest', 'test@test.com', 'test')
        token, exp = user.encode_auth_token(user.id, is_private_device=True)
        self.assertTrue(isinstance(token, bytes))
        self.assertEqual(User.decode_auth_token(token)[0], user.id)
        self.assertTrue(isinstance(exp, datetime.datetime))


if __name__ == '__main__':
    unittest.main()
