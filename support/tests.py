from django.test import TestCase
from django.contrib.auth.models import User
from .forms import ContactForm
from .apps import SupportConfig

# Create your tests here.

class TestSupportApp(TestCase):
    def setUp(self):
        self.user = {
            'first_name': 'John',
            'last_name': 'Smith',
            'username': 'mspe',
            'email': 'test@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.user)

    def test_support_page_response(self):
        """Test page responpse"""
        response = self.client.get(
            '/support/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Support</h1>', response.content)

    def test_support_app(self):
        """Test Support App"""
        self.assertEqual("support", SupportConfig.name)
    
    def test_contact_post(self):
        """Test post for contact page"""
        response = self.client.post(
            '/support/',
            data={
                'name': 'Matt',
                'email': "test@google.com",
                'subject': "Test Subject",
                'message': "Here is a test message"
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_initial_in_contact_form(self):
        """Test that when a user is logged in their email
        is displayed automatically in the contact form"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/support/')
        self.assertIn(b'<input type="email" name="email" value="test@gmail.com" class=" form-control" required id="id_email">', response.content)

    def test_invalid_form_in_post(self):
        """Test invalid for data and return variables"""
        response = self.client.post(
            '/support/',
            {
                'name': 'Matt',
                'email': "",
                'subject': "Test Subject",
                'message': "Here is a test message"
            }
        )
        self.assertIn(
            b'This field is required.',
            response.content
        )

class TestContactForm(TestCase):
    """Contact form tests *Commented due to captcha not allowing test currently*"""
    # def test_contact_form_valid_response(self):
    #     """Test full working contact form"""
    #     form = ContactForm({
    #         'name': 'Matt',
    #         'email': 'test@email.com',
    #         'subject': 'test subject',
    #         'message': 'test message'
    #     })
    #     self.assertTrue(form.is_valid())

    def test_contact_form_invalid_email(self):
        """Test full working contact form"""
        form = ContactForm({
            'name': 'Matt',
            'email': 'testemail.com',
            'subject': 'test subject',
            'message': 'test message'
        })
        self.assertFalse(form.is_valid())

    def test_contact_form_invalid_subject(self):
        """Test full working contact form"""
        form = ContactForm({
            'name': 'Matt',
            'email': 'test@email.com',
            'subject': '',
            'message': 'test message'
        })
        self.assertFalse(form.is_valid())

    def test_contact_form_invalid_message(self):
        """Test full working contact form"""
        form = ContactForm({
            'name': 'Matt',
            'email': 'test@email.com',
            'subject': 'test subject',
            'message': ''
        })
        self.assertFalse(form.is_valid())

    def test_contact_form_empty(self):
        """Test empty contact form"""
        form = ContactForm({
            'name': '',
            'email': '',
            'subject': '',
            'message': ''
        })
        self.assertFalse(form.is_valid())