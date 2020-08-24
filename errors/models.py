from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Issue(models.Model):
    """Issues"""
    class categories(models.TextChoices):
        BUG = '1', 'Bug'
        DUPLICATE = '2', 'Duplicate'
        ENHANCEMENT = '3', 'Enhancement'
        WONTFIX = '4', 'Wont Fix'
        QUESTION = '5', 'Question'
        OTHER = '6', 'Other'
    class issueLocation(models.TextChoices):
        HOME = '1', 'Home'
        CREATE = '2', 'Create Build'
        EDIT = '3', 'Edit Build'
        BUILD = '4', 'Delete Build'
        SEARCHING = '5', 'Builds Searching'
        UPDATEPROFILE = '7', 'Updating Profile'
        CHANGINGPASSWORD = '8', 'Changing Password'
        ACCDEACTIVATION = '9', 'Account Deactivation'
        OTHER = '10', 'Other'
    class priority(models.TextChoices):
        LOW = '1', 'Low'
        MEDIUM = '2', 'Medium'
        HIGH = '3', 'High'
        CRITICAL = '4', 'Critical'
        NEW = '5', 'New'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=11, choices=categories.choices, default='1')
    issue_open = models.BooleanField(default=True)
    issue_location = models.CharField(max_length=20, choices=issueLocation.choices, default='10')
    priority = models.CharField(max_length=8, choices=priority.choices, default='5')
    description = models.TextField()
    admin_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.issue_open:
            r = f'{self.id} - {self.priority} | Open'
        else:
            r = f'{self.id} - {self.priority} | Closed'
        return r
