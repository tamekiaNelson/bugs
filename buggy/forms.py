from django import forms
from buggy.models import Bug


class Ticket(forms.ModelForm):
    class Meta:
        model = Bug
        fields = [
            'title',
            'description',
        ]


class EditTicket(forms.ModelForm):
    class Meta:
        model = Bug
        fields = [
            'title',
            'description',
            'status',
        ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
