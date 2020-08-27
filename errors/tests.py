from django.test import TestCase
from django.contrib.auth.models import User
from .forms import NewComment, NewTicket
from .models import Issue, Comments
from .apps import ErrorsConfig

# Create your tests here.

class TestErrorsApp(TestCase):
    def test_errors_app(self):
        """Test Errors App"""
        self.assertEqual("errors", ErrorsConfig.name)

class TestForms(TestCase):
    """Test forms in Errors App"""
    def test_newcomment_form_valid_response(self):
        """Test full working new comment form."""
        form = NewComment({
            'comment': 'Here is a new comment'
        })
        self.assertTrue(form.is_valid())

    def test_newcomment_form_no_content(self):
        """Test newcomment form with no data"""
        form = NewComment({
            'comment': ''
        })
        self.assertFalse(form.is_valid())

    def test_newticket_form_valid_response(self):
        """Test NewTicket Form with valid response"""
        form = NewTicket({
            'issue_location': '3',
            'description': 'A detailed description'
        })
        self.assertTrue(form.is_valid())

    def test_newticket_form_invalid_response(self):
        """Test NewTicket Form with invalid response"""
        form = NewTicket({
            'issue_location': '3',
            'description': ''
        })
        self.assertFalse(form.is_valid())

class TestModels(TestCase):
    def setUp(self):
        self.user = {
            'first_name': 'John',
            'last_name': 'Smith',
            'username': 'mspe',
            'email': 'test@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.user)
    
    """Test Issues and Comments Models"""
    def __str__issue_model(self):
        """Test __str__ return on issues model"""
        user = User.objects.get(username="mspe")
        response = Issue.objects.create(
            user=user,
            category='1',
            issue_location='2',
            description='Test Model'
        )
        self.assertEqual(str(response), '1 - New | Open')

    def __str__issue_closed(self):
        """Test creation of issues object closed"""
        user = User.objects.get(username="mspe")
        response = Issue.objects.create(
            user=user,
            category='3',
            issue_open=False,
            issue_location='10',
            description='Test 3'
        )
        self.assertEqual(str(response), '2 - New | Closed')

    def create_issue(self):
        """Test creation of issues object open"""
        user = User.objects.get(username="mspe")
        response = Issue.objects.create(
            user=user,
            category='3',
            issue_location='10',
            description='Test 2'
        )
        self.assertEqual(response.user.username, 'mspe')
        self.assertEqual(response.get_category_display(), 'Enhancement')
        self.assertTrue(response.issue_open)
        self.assertEqual(response.get_issue_location_display(), 'Other')
        self.assertEqual(response.get_priority_display(), 'New')
        self.assertEqual(response.description, 'Test 2')
        self.assertEqual(response.admin_notes, None)

    def __str__comment_model(self):
        """Test __str__ return on comments model"""
        user = User.objects.get(username="mspe")
        issue = Issue.objects.get(id=1)
        response = Comments.objects.create(
            user=user,
            issue=issue,
            comment='Another comment for issue 1'
        )
        self.assertEqual(response.user.username, 'mspe')
        self.assertEqual(response.issue.id, 1)
        self.assertEqual(response.comment, 'Another comment for issue 1')
    
    def create_comment(self):
        """Test creation comments object"""
        user = User.objects.get(username="mspe")
        issue = Issue.objects.get(id=1)
        response = Comments.objects.create(
            user=user,
            issue=issue,
            comment='Comment for issue 1'
        )
        self.assertEqual(str(response), 'Issue 1 comment by mspe')

    def test_models_in_order(self):
        self.__str__issue_model()
        self.__str__issue_closed()
        self.__str__comment_model()
        self.create_issue()
        self.create_comment()

class TestPageRespones(TestCase):
    """Test Page & URL responses"""
    def setUp(self):
        self.user = {
            'first_name': 'John',
            'last_name': 'Smith',
            'username': 'mspe',
            'email': 'test@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.user)

    def test_issue_tracker_response_get(self):
        response = self.client.get('/i/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Issue Tracker</h1>', response.content)

    def issue_tracker_response_post(self):
        """Test post to create new ticket"""
        self.client.post(
            '/u/login/',
            self.user,
            follow=True
        )
        response = self.client.post(
            '/i/',
            {
                'issue_location': '1',
                'description': 'Test post description'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<td>4</td>', response.content)

    def issue_detail_get(self):
        """Test response of issue detail"""
        response = self.client.get('/i/4')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Issue 4</h1>', response.content)

    def add_comment_post(self):
        """Test adding a comment to an issue"""
        self.client.post(
            '/u/login/',
            self.user,
            follow=True
        )
        response = self.client.post(
            '/i/comment/add/4',
            {
                'comment': 'Test comment for issue'
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn(b'Comment has been added.', response.content)
        self.assertIn(b'Test comment for issue', response.content)

    def test_add_comment_get_should_redirect(self):
        """test the add comment get response, should be a redirect"""
        self.client.post(
            '/u/login/',
            self.user,
            follow=True
        )
        response = self.client.get(
            '/i/comment/add/4'
        )
        self.assertEquals(response.status_code, 302)
    
    def delete_comment(self):
        """Test deleting a comment"""
        self.client.post(
            '/u/login/',
            self.user,
            follow=True
        )
        response = self.client.get(
            '/i/comment/delete/3',
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comment has been deleted.', response.content)

    def test_issue_get_post_in_order(self):
        self.issue_tracker_response_post()
        self.issue_detail_get()
        self.add_comment_post()
        self.delete_comment()