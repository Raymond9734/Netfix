from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import date, timedelta

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    """Custom DateInput widget that renders as HTML5 date input"""
    input_type = "date"


def validate_email(value):
    """
    Validate that email is not already taken
    Args:
        value: Email to validate
    Raises:
        ValidationError if email exists
    """
    # Check if email exists in User model
    if User.objects.filter(email=value).exists():
        raise ValidationError(f"{value} is already taken.")


class UserLoginForm(forms.Form):
    """
    Form for user login with email/username and password.
    Allows login with either email or username.
    """
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter Username"})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter Email",
                "autocomplete": "off"  # Prevent browser autofill
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter Password"})
    )
    user_type = forms.ChoiceField(
        choices=[("company", "Company"), ("customer", "Customer")],
        widget=forms.RadioSelect,
    )

    def clean(self):
        """
        Validate form data and authenticate user.
        Performs the following checks:
        1. Validates required fields are present
        2. Finds user by email or username
        3. Authenticates credentials
        4. Verifies user type matches account type
        
        Returns:
            dict: Cleaned form data
        Raises:
            ValidationError: If validation fails
        """
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email") 
        password = cleaned_data.get("password")
        user_type = cleaned_data.get("user_type")

        # Validate required fields
        if not username:
            raise ValidationError("Username  is required.")
        if not email:
            raise ValidationError("Email is required")
        if not password:
            raise ValidationError("Password is required.")

        # Find and validate user
        user = None
        
        # Try to find user by email first
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError("No user found with this email.")

        # Then validate username matches if provided
        if username:
            try:
                potential_user = User.objects.get(username=username)
                if user is None:
                    user = potential_user
                elif user != potential_user:
                    raise ValidationError("Username and email do not match.")
            except User.DoesNotExist:
                raise ValidationError("No user found with this username.")

        if user:
            # Authenticate credentials and validate user type
            user = authenticate(username=user.username, password=password)
            if user is None:
                raise ValidationError("Invalid username or password.")
                
            # Check if user type matches account type
            if (user.is_company and user_type != "company") or \
               (user.is_customer and user_type != "customer"):
                raise ValidationError("User type mismatch.")

        return cleaned_data


class CompanyRegistrationForm(forms.ModelForm):
    """
    Form for company registration.
    Handles company account creation with profile details.
    """
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )
    field_of_work = forms.ChoiceField(
        choices=Company.SERVICE_CHOICES,  # Use predefined choices from model
        label="Field of Work",
    )

    class Meta:
        model = Company
        fields = [
            "email",
            "username",
            "field_of_work",
            "description",
        ]

    def clean_email(self):
        """
        Validate company email is unique
        Returns:
            str: Validated email
        Raises:
            ValidationError: If email already exists
        """
        email = self.cleaned_data.get("email")
        if Company.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        """
        Validate form data, ensuring passwords match
        Returns:
            dict: Cleaned form data
        Raises:
            ValidationError: If passwords don't match
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class CustomerRegistrationForm(forms.ModelForm):
    """
    Form for customer registration.
    Handles customer account creation with profile details.
    """
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )

    # Calculate minimum age date (3 years)
    today = date.today()
    max_date = today - timedelta(days=365 * 3)

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "max": max_date.strftime("%Y-%m-%d"),  # Set maximum allowed date
            }
        ),
        label="Date of Birth",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password_confirmation",
        ]

    def clean_email(self):
        """
        Validate customer email is unique
        Returns:
            str: Validated email
        Raises:
            ValidationError: If email already exists
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        """
        Validate form data, ensuring passwords match
        Returns:
            dict: Cleaned form data
        Raises:
            ValidationError: If passwords don't match
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            self.add_error("password_confirmation", "Passwords do not match.")

        return cleaned_data
