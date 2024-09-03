from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Company
from users.forms import CompanyRegistrationForm

User = get_user_model()

class RegisterCompanyViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("register_company")  # Adjust the URL name if necessary

    def test_register_company_valid_form(self):
        data = {
            "username": "testcompany",
            "email": "testcompany@example.com",
            "password": "testpassword123",
            "password_confirmation": "testpassword123",
            "field_of_work": "Carpentry",  # Adjust to match your choices
        }
        response = self.client.post(self.url, data)

        # Check if the user is redirected to the home page
        self.assertRedirects(response, reverse("main:home"))

        # Check if the user was created in the database
        self.assertTrue(User.objects.filter(username="testcompany").exists())
        user = User.objects.get(username="testcompany")
        self.assertTrue(user.check_password("testpassword123"))
        self.assertTrue(user.is_company)
        self.assertTrue(Company.objects.filter(user=user).exists())
        company = Company.objects.get(user=user)
        self.assertEqual(company.field_of_work, "Carpentry")

    def test_register_company_invalid_form(self):
        data = {
            "username": "",  # Invalid username
            "email": "testcompany@example.com",
            "password": "testpassword123",
            "password_confirmation": "testpassword123",
            "field_of_work": "engineering",  # Invalid field of work
        }
        response = self.client.post(self.url, data)

        # Check if the form errors are returned
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        self.assertContains(response, "Select a valid choice.")
        self.assertFalse(User.objects.filter(email="testcompany@example.com").exists())
        self.assertFalse(Company.objects.filter(email="testcompany@example.com").exists())

    def test_register_company_missing_password_confirmation(self):
        data = {
            "username": "testcompany",
            "email": "testcompany@example.com",
            "password": "testpassword123",
            "password_confirmation": "",  # Missing password confirmation
            "field_of_work": "Carpentry",  # Adjust to match your choices
        }
        response = self.client.post(self.url, data)

        # Check if the form errors are returned
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        self.assertFalse(User.objects.filter(username="testcompany").exists())
        self.assertFalse(Company.objects.filter(email="testcompany@example.com").exists())
