from django import forms
from buggy.models import Bugs


class Ticket(forms.ModelForm):
    class Meta:
        model = Bugs
        fields = [
            'user_ticket_creator',
            'Title',
            'Description',
            'Status'
        ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
