from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from .models import UserProfile

class SignUpForm(forms.Form):
    ACCOUNT_TYPES = (
        ('creator', 'Campaign Creator'),
        ('donator', 'Donator'),
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control sign__form-input',
            'placeholder': 'Enter your first name',
        })
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control sign__form-input',
            'placeholder': 'Enter your last name',
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control sign__form-input',
            'placeholder': 'Enter your email',
        })
    )

    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-control sign__form-input',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control sign__form-input',
            'placeholder': 'Create a password',
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control sign__form-input',
            'placeholder': 'Confirm your password',
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email
    
    def clean_account_type(self):
        account_type = self.cleaned_data.get('account_type')
        valid_types = dict(self.ACCOUNT_TYPES).keys()

        if not account_type: 
            raise ValidationError('Please select an account type.')
        
        if account_type not in valid_types: 
            raise ValidationError('Please select a valid account type.')
        
        return account_type

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            # Use Django's password validation
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(list(e.messages))
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError({
                    'confirm_password': 'Passwords do not match.'
                })
        
        return cleaned_data

    @transaction.atomic
    def save(self):
        if self.is_valid():
            user = User.objects.create_user(
                username=self.cleaned_data['email'],  # Using email as username
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )

            UserProfile.objects.create(
                user=user,
                account_type=self.cleaned_data['account_type']
            )
            return user
        return None
