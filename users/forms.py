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
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Enter Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter Password"})
    )

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["autocomplete"] = "off"


# Form for handling user registration and validation
class CompanyRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
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
        ]
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "field_of_work"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
