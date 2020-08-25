from django.test import TestCase
from .forms import ContactForm
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
    
    def test_contact_post(self):
        """Test post for contact page"""
        response = self.client.post(
            '/s/',
            data={
                'email': "test@google.com",
                'subject': "Test Subject",
                'message': "Here is a test message"
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_form_in_post(self):
        """Test invalid for data and return variables"""
        response = self.client.post(
            '/s/',
            {
                'email': "",
                'subject': "Test Subject",
                'message': "Here is a test message"
            }
        )
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'sent': False,
                'error': 'Invalid Form'
            }
        )

class TestContactForm(TestCase):
    """Contact form tests"""
    def test_contact_form_valid_response(self):
        """Test full working contact form"""
        form = ContactForm({
            'email': 'test@email.com',
            'subject': 'test subject',
            'message': 'test message'
        })
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid_email(self):
        """Test full working contact form"""
        form = ContactForm({
            'email': 'testemail.com',
            'subject': 'test subject',
            'message': 'test message'
        })
        self.assertFalse(form.is_valid())

    def test_contact_form_invalid_subject(self):
        """Test full working contact form"""
        form = ContactForm({
            'email': 'test@email.com',
            'subject': '',
            'message': 'test message'
        })
        self.assertFalse(form.is_valid())

    def test_contact_form_invalid_message(self):
        """Test full working contact form"""
        form = ContactForm({
            'email': 'test@email.com',
            'subject': 'test subject',
            'message': ''
        })
        self.assertFalse(form.is_valid())

    def test_contact_form_empty(self):
        """Test empty contact form"""
        form = ContactForm({
            'email': '',
            'subject': '',
            'message': ''
        })
        self.assertFalse(form.is_valid())