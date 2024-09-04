from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class TranslationForm(forms.Form):
    pdf_file = forms.FileField(label='Select a PDF file')
    direction = forms.ChoiceField(
        choices=[('ms-en', 'Malay to English'), ('en-ms', 'English to Malay')],
        label='Translation Direction'
    )

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        min_length=6,
        validators=[
            RegexValidator(
                regex='^[\\w.@+-]+$',  # Allows letters, digits, and specified special characters
                message='Minimum 6 characters and must contain only letters, digits, and @/./+/-/_'
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'autocomplete': 'username'
        }),
        help_text='Minimum 6 characters and must contain only letters, digits, and @/./+/-/_',
        label='Username <span class="required-asterisk">*</span>'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'autocomplete': 'email'
        }),
        label='Email <span class="required-asterisk">*</span>'
    )
    password1 = forms.CharField(
        min_length=12,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'autocomplete': 'new-password'
        }),
        help_text='Minimum 12 characters and must contain only letters, digits, and @/./+/-/_',
        label='Password <span class="required-asterisk">*</span>'
    )
    password2 = forms.CharField(
        min_length=12,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'autocomplete': 'new-password'
        }),
        help_text='Re-enter the password.',
        label='Confirm Password <span class="required-asterisk">*</span>'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'autocomplete': 'username'
        }),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'autocomplete': 'current-password'
        }),
        label='Password'
    )
#this is final project