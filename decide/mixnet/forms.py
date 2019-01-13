from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())