from django.test import TestCase
from .apps import SupportConfig

# Create your tests here.

class TestSupportApp(TestCase):
    def test_support_page_response(self):
        """Test page responpse"""
        response = self.client.get(
            '/s/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Support</h1>', response.content)

    def test_support_app(self):
        """Test Support App"""
        self.assertEqual("support", SupportConfig.name)