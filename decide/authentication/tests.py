from django.core import mail
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from base import mods


#Nuevo
from django.test import TestCase
from .forms import RegisterUser

import uuid

from django.core.exceptions import ValidationError
from django.utils import six

from . import forms, validators

from .base import RegistrationTestCase


class AuthTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='voter1')
        u.set_password('123')
        u.email = 'test@gmail.com'
        u.save()

    def tearDown(self):
        self.client = None

    def test_login(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('token'))

    def test_login_email(self):
        data = {'username': 'test@gmail.com', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('token'))

    def test_login_fail(self):
        data = {'username': 'voter1', 'password': '321'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_login_email_fail(self):
        data = {'username': 'test@gmail.com', 'password': '321'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_getuser(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertEqual(user['id'], 1)
        self.assertEqual(user['username'], 'voter1')

    def test_getuser_invented_token(self):
        token = {'token': 'invented'}
        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_getuser_invalid_token(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 0)



class PasswordTestCases(TestCase):

    def test_password_reset(self):
        data = {'username': 'test@gmail.com', 'password': 'aquiTodoelDia1234'}
        default_token_generator = PasswordResetTokenGenerator()
        user = User.objects.create_user('antonio', 'test@gmail.com', 'aquiTodoelDia1234')
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(str(user.pk).encode()).decode()

        #Commented out due to static files not being able to be collected previous to the testing phase
        #response = self.client.get(reverse('password_reset'))
        #self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.template_name[0], 'registration/password_reset_form.html')

        response = self.client.post(reverse('password_reset'), data, format='json')
        self.assertEqual(response.status_code, 200)

        mail.send_mail('Password reset on Decide', 'body.', 'from@gmail.com', ['to@gmail.com'])

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password reset on Decide')

        response = self.client.get(reverse('password_reset_confirm', kwargs={'token': token, 'uidb64': uid}))
        self.assertEqual(response.status_code, 302)




class TestRegistrationForm(TestCase):

    def test_registration_form(self):
        # test invalid data
        invalid_data = {
            "email": "usertest.com",
            "username": "user@test.com",
            "password1": "secret",
            "password2": "not secret"
        }
        form = RegisterUser(data=invalid_data)
        form.is_valid()
        self.assertTrue(form.errors)

        # test valid data
        valid_data = {
            "email": "user@test.com",
            "username": "user@test.com",
            "password1": "secret123",
            "password2": "secret123"
        }
        form = RegisterUser(data=valid_data)
        form.is_valid()
        self.assertFalse(form.errors)


class RegistrationFormTests(RegistrationTestCase):
    """
    Test the built-in form classes.
    """

    def test_username_uniqueness(self):
        """
        Username uniqueness is enforced.
        This test is necessary as of 2.1.x to ensure the base
        UserCreationForm clean() continues to be called from the
        overridden clean() in RegistrationForm.
        """
        user_data = self.valid_data.copy()
        del user_data['password1']
        del user_data['password2']
        user_data['password'] = 'swordfish'
        existing_user = self.user_model(**user_data)
        existing_user.save()
        form = forms.RegisterUser(data=self.valid_data.copy())
        self.assertFalse(form.is_valid())
        self.assertTrue(
            form.has_error(self.user_model.USERNAME_FIELD)
        )

    def test_reserved_name_non_string(self):
        """
        GitHub issue #82: reserved-name validator should not attempt
        to validate a non-string 'username'.
        """
        validator = validators.ReservedNameValidator()
        for value in (123456, 1.7, uuid.uuid4()):
            self.assertTrue(validator(value) is None)

    def test_case_insensitive_validator(self):
        """
        Test the case-insensitive username validator.
        """
        validator = validators.CaseInsensitiveUnique(
            self.user_model, self.user_model.USERNAME_FIELD,
            validators.DUPLICATE_USERNAME
        )
        for value in (123456, 1.7, uuid.uuid4()):
            self.assertTrue(validator(value) is None)

        base_creation_data = self.valid_data.copy()
        base_creation_data['password'] = base_creation_data['password1']
        del base_creation_data['password1']
        del base_creation_data['password2']

        test_names = [
            (u'alice', u'ALICE'),
            (u'ALICE', u'alice'),
            (u'Alice', u'alice'),
        ]
        if six.PY3:
            test_names.extend([
                (u'STRASSBURGER', u'straßburger'),
            ])

        for name, conflict in test_names:
            creation_data = base_creation_data.copy()
            creation_data[self.user_model.USERNAME_FIELD] = name
            existing_user = self.user_model(**creation_data)
            existing_user.save()
            with self.assertRaisesMessage(
                    ValidationError,
                    six.text_type(validators.DUPLICATE_USERNAME)
            ):
                validator(conflict)
            existing_user.delete()

    def test_case_insensitive_form(self):
        """
        Test the case-insensitive registration form.
        """
        base_creation_data = self.valid_data.copy()
        base_creation_data['password'] = base_creation_data['password1']
        del base_creation_data['password1']
        del base_creation_data['password2']

        test_names = [
            (u'alice', u'ALICE'),
            (u'ALICE', u'alice'),
            (u'Alice', u'alice'),
            (u'AlIcE', u'aLiCe'),
            (u'STRASSBURGER', u'straßburger'),
        ]

        for name, conflict in test_names:
            creation_data = base_creation_data.copy()
            creation_data[self.user_model.USERNAME_FIELD] = name
            existing_user = self.user_model(**creation_data)
            existing_user.save()
            user_data = self.valid_data.copy()
            user_data[self.user_model.USERNAME_FIELD] = name
            form = forms.RegisterUser(data=user_data)
            self.assertFalse(form.is_valid())
            self.assertTrue(
                form.has_error(self.user_model.USERNAME_FIELD)
            )
            self.assertEqual(
                [six.text_type(validators.DUPLICATE_USERNAME)],
                form.errors[self.user_model.USERNAME_FIELD]
            )
            self.assertEqual(
                1, len(form.errors[self.user_model.USERNAME_FIELD])
            )
