import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Customer, Company
from django.core.exceptions import ValidationError

User = get_user_model()

class UserModelTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
            is_customer=True
        )

    def test_user_creation(self):
        user = User.objects.get(username="testuser")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.is_customer)
        self.assertFalse(user.is_company)

class CustomerModelTests(TestCase):
    def setUp(self):
        # Create a user and a customer instance
        self.user = User.objects.create_user(
            username="customeruser",
            email="customeruser@example.com",
            password="customerpassword123",
            is_customer=True
        )
        self.customer = Customer.objects.create(
            user=self.user,
            date_of_birth="1990-01-01"
        )

    def test_customer_creation(self):
        customer = Customer.objects.get(user=self.user)
        self.assertEqual(customer.user.username, "customeruser")
        self.assertEqual(customer.date_of_birth, datetime.date(1990, 1, 1))

    def test_customer_str(self):
        self.assertEqual(str(self.customer), "customeruser")

class CompanyModelTests(TestCase):
    def setUp(self):
        # Create a user and a company instance
        self.user = User.objects.create_user(
            username="companyuser",
            email="companyuser@example.com",
            password="companypassword123",
            is_company=True
        )
        self.company = Company.objects.create(
            user=self.user,
            email="companyuser@example.com",
            username="companyuser",
            field_of_work="Locks",
            description="A company providing Locks solutions."
        )

    def test_company_creation(self):
        company = Company.objects.get(user=self.user)
        self.assertEqual(company.user.username, "companyuser")
        self.assertEqual(company.email, "companyuser@example.com")
        self.assertEqual(company.field_of_work, "Locks")
        self.assertEqual(company.description, "A company providing Locks solutions.")
    
    def test_company_str(self):
        self.assertEqual(str(self.company), f"{self.user.id} - {self.user.username}")

    def test_email_unique(self):
        with self.assertRaises(ValidationError):
            company = Company(
                user=self.user,
                email="companyuser@example.com",  # Duplicate email
                username="anothercompanyuser",
                field_of_work="Gardening",
                description="Another company providing Gardening solutions."
            )
            company.full_clean()  # This should raise a ValidationError

    def test_rating_validators(self):
        company = Company(
            user=self.user,
            email="newcompany@example.com",
            username="newcompanyuser",
            field_of_work="Electricity",
            description="A new company providing Electricity solutions.",
            rating=-1  # Invalid rating
        )
        with self.assertRaises(ValidationError):
            company.full_clean()  # This should raise a ValidationError

        company.rating = 6  # Invalid rating
        with self.assertRaises(ValidationError):
            company.full_clean()  # This should also raise a ValidationError
