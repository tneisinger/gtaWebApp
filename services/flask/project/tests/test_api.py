# services/flask/project/tests/test_admin.py

import json
import unittest

from project.tests.base import BaseTestCase


class TestApiService(BaseTestCase):
    """Tests the RESTful api"""

    def test_ping(self):
        """Ensure that the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])


if __name__ == '__main__':
    unittest.main()
