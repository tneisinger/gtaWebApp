import json

from project.tests.base import BaseTestCase


class TestAdminApiGeneral(BaseTestCase):
    """General tests for the Admin Api Service."""

    def test_ping(self):
        """Ensure that the /admin/ping route behaves correctly."""
        response = self.client.get('/admin/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])
