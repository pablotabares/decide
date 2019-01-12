from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from . import validators


class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        ]

    def clean_email(self, commit=True):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise ValidationError('Email is already registered.')
        return email


class RegistrationFormUniqueEmail(UserCreationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.
    """
    def __init__(self, *args, **kwargs):
        super(RegistrationFormUniqueEmail, self).__init__(*args, **kwargs)
        email_field = User.get_email_field_name()
        self.fields[email_field].validators.append(
            validators.CaseInsensitiveUnique(
                User, email_field,
                validators.DUPLICATE_EMAIL
            )
        )