from django import forms
from .models import Issue, Comments

class NewTicket(forms.ModelForm):
    """Form for new ticket from model"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['placeholder'] = 'Please describe in much detail as possible your actions leading to this issue or the proposed enhancement.'

    class Meta: 
        model = Issue
        fields = [
            'issue_location',
            'description'
        ]

class NewComment(forms.ModelForm):
    """Add a new comment"""
    class Meta:
        model = Comments
        fields = [
            'comment'
        ]