from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = "date"


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
    pass


class CompanySignUpForm(UserCreationForm):
    pass


class UserLoginForm(forms.Form):
    username = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "Enter Username"})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Email", "autocomplete": "off"}
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
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        user_type = cleaned_data.get("user_type")

        # Check if either username or email is provided
        if not username:
            raise ValidationError("Username  is required.")
        if not email:
            raise ValidationError("Email is required")
        if not password:
            raise ValidationError("Password is required.")

        # Find user by email or username
        user = None
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError("No user found with this email.")

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
            # Authenticate the user
            user = authenticate(username=user.username, password=password)
            if user is None:
                raise ValidationError("Invalid username or password.")
            if user.is_company and user_type != "company":
                raise ValidationError("User type mismatch.")
            if user.is_customer and user_type != "customer":
                raise ValidationError("User type mismatch.")

        return cleaned_data


# Form for handling user registration and validation
class CompanyRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )
    field_of_work = forms.ChoiceField(
        choices=[
            ("Air Conditioner", "Air Conditioner"),
            ("All in One", "All in One"),
            ("Carpentry", "Carpentry"),
            ("Electricity", "Electricity"),
            ("Gardening", "Gardening"),
            ("Home Machines", "Home Machines"),
            ("House Keeping", "House Keeping"),
            ("Interior Design", "Interior Design"),
            ("Locks", "Locks"),
            ("Painting", "Painting"),
            ("Plumbing", "Plumbing"),
            ("Water Heaters", "Water Heaters"),
        ],
        label="Field of Work",
    )

    class Meta:
        model = Company
        fields = [
            "email",
            "username",
            "field_of_work",
            "description",
        ]  # Adjusted to Company model fields

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Company.objects.filter(
            email=email
        ).exists():  # Ensure you're checking the right model
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="Date of Birth"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password_confirmation",
            # Note: 'date_of_birth' is not part of the User model, but we will handle it separately
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            self.add_error("password_confirmation", "Passwords do not match.")

        return cleaned_data
