from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django import forms
from django.contrib import admin


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds fields to distinguish between company and customer accounts.
    """
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)


class Customer(models.Model):
    """
    Customer profile model linked to User model.
    Stores additional customer-specific information.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )
    date_of_birth = models.DateField(
        help_text="Customer's date of birth"
    )

    def __str__(self):
        return self.user.username


class Company(models.Model):
    """
    Company profile model linked to User model.
    Stores company-specific information and service details.
    """
    # Define service choices as class constant for reusability
    SERVICE_CHOICES = (
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
    )

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='company_profile'
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        default="default@example.com",
        help_text="Company contact email"
    )
    username = models.CharField(
        max_length=150, 
        unique=True,
        help_text="Company username for identification"
    )
    field_of_work = models.CharField(
        max_length=70,
        choices=SERVICE_CHOICES,
        help_text="Primary service category offered by the company"
    )
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        default=0,
        help_text="Company rating from 0 to 5"
    )
    description = models.TextField(
        blank=True, 
        null=True,
        help_text="Detailed description of company services"
    )

    def __str__(self):
        return f"{self.user.id} - {self.user.username}"
