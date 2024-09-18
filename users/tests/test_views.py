from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from users.models import Company, Customer

User = get_user_model()


class UserViewTests(TestCase):
    def setUp(self):
        self.company_registration_url = reverse("users:register_company")
        self.customer_registration_url = reverse("users:register_customer")
        self.login_url = reverse("users:login")
        self.choose_registration_url = reverse("users:choose_registration")

        # Create a user for login tests
        self.user_password = "testpassword123"
        self.company_user = User.objects.create_user(
            username="companyuser",
            email="company@test.com",
            password=self.user_password,
            is_company=True,
        )

        # Create a Company instance linked to the company user
        self.company = Company.objects.create(
            user=self.company_user,
            username="companyuser",
            email="company@test.com",
            field_of_work="IT Services",
            description="A company providing IT solutions."
        )

        self.customer_user = User.objects.create_user(
            username="customeruser",
            email="customer@test.com",
            password=self.user_password,
            is_customer=True,
        )
        # Create a Customer instance linked to the customer user
        self.customer = Customer.objects.create(
            user=self.customer_user,
            date_of_birth="1990-01-01",
        )

    def test_choose_registration_view(self):
        response = self.client.get(self.choose_registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_choice.html")

    def test_register_company_valid(self):
        form_data = {
            "username": "newcompany",
            "email": "newcompany@test.com",
            "password": "newpassword123",
            "password_confirmation":"newpassword123",
            "field_of_work": "Locks",
            "description": "A new company providing Locks solutions.",
        }
        response = self.client.post(self.company_registration_url, form_data)
        self.assertEqual(
            response.status_code, 302
        )  # Expect redirect on successful registration
        self.assertTrue(User.objects.filter(username="newcompany").exists())
        self.assertTrue(Company.objects.filter(username="newcompany").exists())
        self.assertRedirects(
            response, reverse("company_profile", kwargs={"name": "newcompany"})
        )

    def test_register_company_invalid(self):
        form_data = {
            "username": "",  # Invalid data (username is required)
            "email": "invalidemail@test.com",
            "password": "newpassword123",
            "password_confirmation":"newpassword123",
            "field_of_work": "IT Services",
        }
        response = self.client.post(self.company_registration_url, form_data)
        self.assertEqual(response.status_code, 200)  # Form errors should not redirect
        self.assertFalse(User.objects.filter(email="invalidemail@test.com").exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Please correct the errors below.")

    def test_register_customer_valid(self):
        form_data = {
            "username": "newcustomer",
            "email": "newcustomer@test.com",
            "password": "newpassword123",
            "password_confirmation":"newpassword123",
            "date_of_birth": "1990-01-01",
        }
        response = self.client.post(self.customer_registration_url, form_data)
        self.assertEqual(
            response.status_code, 302
        )  # Expect redirect on successful registration
        self.assertTrue(User.objects.filter(username="newcustomer").exists())
        self.assertTrue(Customer.objects.filter(user__username="newcustomer").exists())
        self.assertRedirects(response, reverse("main:home"))

    def test_register_customer_invalid(self):
        form_data = {
            "username": "",  # Invalid data (username is required)
            "email": "invalidcustomer@test.com",
            "password": "newpassword123",
            "password_confirmation":"newpassword123",
            "date_of_birth": "1990-01-01",
        }
        response = self.client.post(self.customer_registration_url, form_data)
        self.assertEqual(response.status_code, 200)  # Form errors should not redirect
        self.assertFalse(User.objects.filter(email="invalidcustomer@test.com").exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Please correct the errors below.")

    # Test login using username and email for company
    def test_login_view_company_valid(self):
        form_data = {
            "username": "companyuser",
            "email": "company@test.com",
            "password": self.user_password,
            "user_type": "company",
        }
        response = self.client.post(self.login_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("company_profile", kwargs={"name": "companyuser"})
        )

    # Test login using email for company
    def test_login_view_company_email_valid(self):
        form_data = {
            "username": "companyuser",
            "email": "company@test.com",
            "password": self.user_password,
            "user_type": "company",
        }
        response = self.client.post(self.login_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("company_profile", kwargs={"name": "companyuser"})
        )

    # Test login using username and email for customer
    def test_login_view_customer_valid(self):
        form_data = {
            "username": "customeruser",
            "email": "customer@test.com",
            "password": self.user_password,
            "user_type": "customer",
        }
        response = self.client.post(self.login_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("customer_profile", kwargs={"name": "customeruser"})
        )

    # Test login using email for customer
    def test_login_view_customer_email_valid(self):
        form_data = {
            "username": "customeruser",
            "email": "customer@test.com",
            "password": self.user_password,
            "user_type": "customer",
        }
        response = self.client.post(self.login_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("customer_profile", kwargs={"name": "customeruser"})
        )

    # Test invalid login
    def test_login_view_invalid(self):
        form_data = {
            "username": "wrongusername",
            "email": "wrongemail@test.com",
            "password": "wrongpassword",
            "user_type": "company",
        }
        response = self.client.post(self.login_url, form_data)
        self.assertEqual(
            response.status_code, 200
        )  # Invalid credentials should not redirect
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Please correct the errors below.")
