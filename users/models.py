from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django import forms
from django.contrib import admin


# Custom User model
class User(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # Use OneToOneField for a one-to-one relationship
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username


# Company model
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        default="default@example.com",
    )
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    field_of_work = models.CharField(
        max_length=70,
        choices=(
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
        ),
        blank=False,
        null=False,
    )
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(0)], default=0
    )

    def __str__(self):
        return f"{self.user.id} - {self.user.username}"
