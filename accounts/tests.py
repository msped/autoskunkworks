from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django import forms
from builds.models import *
from builds.utils import create_build_id
from .forms import UserLoginForm, UserRegisterForm
from .apps import AccountsConfig

# Create your tests here.

class AccountViewsTest(TestCase):
    """Test for Account Views"""

    def setUp(self):
        self.user = {
            'first_name': 'John',
            'last_name': 'Smith',
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'testpassword'
        }
        self.user2 = {
            'username': 'test2',
            'email': 'test2@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.user)
        User.objects.create_user(**self.user2)

    def test_login_page_response(self):
        """Test response of login page when not logged in"""
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_response_logged_in(self):
        """test response of the login age if the user is logged in
        should redirect (302 response)"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/user/login/', follow=True)
        self.assertIn(
            b'<h1 class="display-5">Plan your builds with AutoSkunkWorks.</h1>',
            response.content
        )

    def test_login_with_inccorect_details(self):
        """Test login with incorrect details"""
        response = self.client.post(
            '/user/login/',
            {
                'username': 'notauser',
                'password': 'examplepassword'
            },
            follow=True
        )
        self.assertIn(b'Your username or password are incorrect', response.content)

    def test_logout_when_user_logged_in(self):
        """Test logout function"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/user/logout/', follow=True)
        self.assertIn(b'<h1 class="login-header text-center">Login</h1>', response.content)

    def test_logout_when_logged_out(self):
        """Test where the logout view should return to login page if
        no user logged in"""
        response = self.client.get('/user/logout/', follow=True)
        self.assertIn(b'<h1 class="login-header text-center">Login</h1>', response.content)


    def test_register_when_not_logged_in(self):
        """Test register page when a user isnt logged in"""
        response = self.client.get('/user/register/')
        self.assertIn(b'<h1 class="register-header text-center">Register</h1>', response.content)

    def test_register_when_logged_in(self):
        """Test register page when a user is logged in
        should redirect (302 response)"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/user/register/', follow=True)
        self.assertIn(
            b'<h1 class="display-5">Plan your builds with AutoSkunkWorks.</h1> ',
            response.content
        )

    def test_successful_registration(self):
        """Test registration of a user (successful)
        should redirect"""
        response = self.client.post(
            '/user/register/',
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'username': 'msped',
                'email': 'test@example.com',
                'password1': 'examplepassword',
                'password2': 'examplepassword'
            },
            follow=True
        )
        self.assertIn(b'You have successfully registered.', response.content)

    def test_change_password_post(self):
        """Test change password post successful"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        response = self.client.post(
            '/user/change-password/',
            {
                'old_password': 'testpassword',
                'new_password1': 'newtestpassword',
                'new_password2': 'newtestpassword'
            },
            follow=True
        )
        self.assertIn(b'Password has been updated', response.content)

    def test_settings_logged_in(self):
        """Test settings page response when a user is logged in, should return settings page"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/user/settings/')
        self.assertIn(b'<h1 class="text-center mb-3">\n    Settings\n</h1>', response.content)

    def test_profile_update(self):
        """test post to update profile items"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        response = self.client.post(
            '/user/update-profile/',
            {
                'first_name': 'Matt',
                'last_name': 'Edwards',
                'email': 'test_email@gmail.com'
            },
            follow=True
        )
        self.assertIn(b'Profile Updated', response.content)

    def test_deactivate_user(self):
        """Test deactivation of a users account"""
        self.client.post(
            '/user/login/',
            self.user2,
            follow=True
        )
        response = self.client.get(
            '/user/delete-account/',
            follow=True
        )
        self.assertIn(b'Account Deactivated. If you wish to create new builds you will have to re-register.', response.content)

    def test_deactivate_user_with_builds(self):
        """Test deletion of users builds when user deactivates account"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        ex_cat = ExteriorCategory.objects.create(
            title="Front Splitter",
            name="front_splitter"
        )
        en_cat = EngineCategory.objects.create(
            title="Remap",
            name="remap"
        )
        ru_cat = RunningCategory.objects.create(
            title="Suspension",
            name="suspension"
        )
        in_cat = InteriorCategory.objects.create(
            title="Harness",
            name="harness"
        )
        Exterior.objects.create(
            exterior_category=ex_cat,
            link='https://carbonwurks.com/shop/exterior/a-class-front-spoiler-extension/',
            price=595.00,
            purchased=True
        )
        Engine.objects.create(
            engine_category=en_cat,
            link='https://www.ebay.co.uk/p/552299957?iid=123190033794&chn=ps&norover=1&mkevt=1&mkrid=710-134428-41853-0&mkcid=2&itemid=123190033794&targetid=909243431449&device=c&mktype=pla&googleloc=1007242&poi=&campaignid=10195651607&mkgroupid=107296279612&rlsatarget=aud-629407027585:pla-909243431449&abcId=1145985&merchantid=7398324&gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zkvDbECip8gnYYYB0idBJnMMNWsLkAU-YrzfCv_4uYdH7rJC-snPUYaAplZEALw_wcB',
            price=849.99,
            purchased=False
        )
        Running.objects.create(
            running_category=ru_cat,
            link='https://www.ebay.co.uk/itm/48-230971-Bilstein-B16-PSS-Coilover-Kit-For-Mercedes-A-Class-12-W176/362936026458?fits=Plat_Gen%3AW176&epid=5013641733&hash=item5480ac455a:g:fWwAAOSwbHpdzQto',
            price=1374.37,
            purchased=False
        )
        Interior.objects.create(
            interior_category=in_cat,
            link='https://www.nickygrist.com/turn-one-6-point-harness?gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zk1hYxZwwU5cFC6Y8EC1L4wJU1uvVCXhhcJ9gFRMdp48FqC7kWGOtAaAiRxEALw_wcB',
            price=119.94,
            purchased=False
        )
        Cars.objects.create(
            make='Mercedes',
            model='A Class',
            trim='A250',
            year='2013',
            price=12500,
            purchased=True
        )
        # create build
        user = User.objects.get(username="test")
        ex = Exterior.objects.all().first()
        en = Engine.objects.all().first()
        ru = Running.objects.all().first()
        inte = Interior.objects.all().first()
        car = Cars.objects.all().first()
        build = Builds.objects.create(
            build_id=create_build_id(),
            author=user,
            name="Test deletion",
            price_hidden=False,
            total=1000,
            private=False,
            car=car
        )
        build.exterior_parts.add(ex)
        build.engine_parts.add(en)
        build.running_gear_parts.add(ru)
        build.interior_parts.add(inte)
        build.likes.add(user)
        response = self.client.get(
            '/user/delete-account/'
        )
        self.assertFalse( Builds.objects.filter(author=user).exists())

    # def test_users_builds_successful(self):
    #     """Test response of a users build"""
    #     response = self.client.get('/user/test/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b"<h1>test's Builds</h1>", response.content)

    def test_users_build_user_doesnt_exists(self):
        """Test invalid user, should redirect"""
        response = self.client.get('/user/doesntexist')
        self.assertEqual(response.status_code, 302)

class AccountFormsTests(TestCase):
    """Test all forms within the accounts app"""

    def setUp(self):
        user = User(
            username='test user',
            email='test@gmail.com',
            password='testpassword'
        )
        user.save()

    def test_register_form_correct_data(self):
        """Test the register form with the correct data"""
        form = UserRegisterForm({
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'test',
            'email': 'test@example.com',
            'password1': 'examplepassword',
            'password2': 'examplepassword',
        })
        self.assertTrue(form.is_valid())

    def test_register_form_existing_email_data(self):
        """Test the register form with the same email data"""
        form = UserRegisterForm({
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'test',
            'email': 'test@gmail.com',
            'password1': 'examplepassword',
            'password2': 'examplepassword',
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,
                                 "Email address must be unique")

    def test_register_form_without_email(self):
        """Test the register form with the correct data"""
        form = UserRegisterForm({
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'test',
            'email': '',
            'password1': 'examplepassword',
            'password2': 'examplepassword',
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,
                                 "Email address is required")

    def test_register_form_without_matching_passwords(self):
        """Test the register form with passwords that aren't matching"""
        form = UserRegisterForm({
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'test',
            'email': 'test@example.com',
            'password1': 'examplepassword',
            'password2': 'examplepassword1',
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,
                                 "Passwords don't match")

    def test_login_form(self):
        """Test login form with correct data"""
        form = UserLoginForm({
            'username': 'test@gmail.com',
            'password': 'testpassword'
        })
        self.assertTrue(form.is_valid())

    def test_login_form_no_email(self):
        """Test for the login form without an email"""
        form = UserLoginForm({
            'username': '',
            'password': 'testpassword'
        })
        self.assertFalse(form.is_valid())

    def test_login_form_no_password(self):
        """Test for the login form without a password"""
        form = UserLoginForm({
            'username': 'test@gmail.com',
            'password': ''
        })
        self.assertFalse(form.is_valid())

class TestAccountsApp(TestCase):
    """Test Accounts App"""
    def test_accounts_app(self):
        """Test Accounts App"""
        self.assertEqual("accounts", AccountsConfig.name)

