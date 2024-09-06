from django.forms import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from services.models import Service
from users.models import Company, Customer
from users.forms import CompanyRegistrationForm, CustomerRegistrationForm, UserLoginForm
from datetime import date
from django.contrib.messages import get_messages

User = get_user_model()


class RegisterCompanyViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = "testcompany1"
        self.email = "company@example.com"
        self.password = "password"
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            is_company=True,
        )
        self.register_url = reverse("register_company")

    # def test_register_company_valid_form(self):
    #     response = self.client.post(
    #         self.register_url,
    #         {
    #             "username": self.username,
    #             "email": self.email,
    #             "password1": self.password,
    #             "password_confirmation": self.password,
    #             "field_of_work": "Engineering",
    #         },
    #     )
    #     self.assertRedirects(
    #         response,
    #         reverse("company_profile", kwargs={"name": self.username}),
    #     )

    # Check if the user was created in the database
    # self.assertTrue(User.objects.filter(username="testcompany").exists())
    # user = User.objects.get(username="testcompany")
    # self.assertTrue(user.check_password("password"))
    # self.assertTrue(user.is_company)
    # self.assertTrue(Company.objects.filter(user=user).exists())
    # company = Company.objects.get(user=user)
    # self.assertEqual(company.field_of_work, "Engineering")  # Correct field value

    def test_register_company_invalid_form(self):
        data = {
            "username": "",  # Invalid username
            "email": "testcompany@example.com",
            "password1": "testpassword123",
            "password_confirmation": "testpassword123",
            "field_of_work": "invalid_field",  # Adjust to match your choices
        }
        response = self.client.post(self.register_url, data)

        # Check if the form errors are returned
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        self.assertContains(response, "Select a valid choice.")
        self.assertFalse(User.objects.filter(email="testcompany@example.com").exists())
        self.assertFalse(
            Company.objects.filter(email="testcompany@example.com").exists()
        )

    def test_register_company_missing_password_confirmation(self):
        data = {
            "username": "testcompany1",
            "email": "testcompany1@example.com",
            "password1": "testpassword123",
            "password_confirmation": "rat",  # Missing password confirmation
            "field_of_work": "Carpentry",
        }
        response = self.client.post(self.register_url, data)

        # Check if the form errors are returned
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        self.assertFalse(User.objects.filter(username="testcompany").exists())
        self.assertFalse(
            Company.objects.filter(email="testcompany1@example.com").exists()
        )


class RegisterCustomerViewTests(TestCase):

    def test_register_customer_success(self):
        # Prepare POST data
        post_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "password_confirmation": "testpassword123",
            "date_of_birth": "2000-01-01",
        }

        # Send POST request to the view
        response = self.client.post(reverse("register_customer"), data=post_data)

        # Check if the user is created
        user = get_user_model().objects.filter(username="testuser").first()
        self.assertIsNotNone(user)

        # Check if the customer is created
        customer = Customer.objects.filter(user=user).first()
        self.assertIsNotNone(customer)

        # Convert the date_of_birth string to a date object and compare
        expected_date = date(2000, 1, 1)
        self.assertEqual(customer.date_of_birth, expected_date)

        # Check if the user is logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Check if the user is redirected to the home page
        self.assertRedirects(response, reverse("main:home"))

    def test_register_customer_invalid_data(self):
        # Prepare invalid POST data (passwords do not match)
        post_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "password_confirmation": "wrongpassword",
            "date_of_birth": "2000-01-01",
        }

        # Send POST request to the view
        response = self.client.post(reverse("register_customer"), data=post_data)

        # Get the form from the response context
        form = response.context["form"]

        # Check that the user is not created
        self.assertFalse(User.objects.filter(username="testuser").exists())

        # Check that the customer is not created
        self.assertFalse(Customer.objects.filter(user__username="testuser").exists())

        # Check that the form has errors
        self.assertFormError(form, "password_confirmation", "Passwords do not match.")

        # Check that the page is rendered again with form errors
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register_customer.html")


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.company_user = User.objects.create_user(
            username="testcompany", email="company@test.com", password="testpass123"
        )
        self.company_user.is_company = True
        self.company_user.save()

        self.company = Company.objects.create(user=self.company_user)

        self.customer_user = User.objects.create_user(
            username="testcustomer", email="customer@test.com", password="testpass123"
        )
        self.customer_user.is_customer = True
        self.customer_user.save()

        # self.service = Service.objects.create(
        #     company=self.company, name="Test Service", date="2023-01-01"
        # )

    def test_company_profile_view(self):
        url = reverse("company_profile", kwargs={"name": self.company_user.username})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
        self.assertEqual(response.context["user"], self.company_user)
        # self.assertQuerysetEqual(response.context["services"], [repr(self.service)])

    def test_login_view_get(self):
        url = reverse("login")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_view_post_company_success(self):
        url = reverse("login")
        data = {
            "username": "testcompany",
            "email": "company@test.com",
            "password": "testpass123",
            "user_type": "company",
        }
        response = self.client.post(url, data)

        self.assertRedirects(
            response,
            reverse("company_profile", kwargs={"name": self.company_user.username}),
        )

    # def test_login_view_post_customer_success(self):
    #     url = reverse("login")
    #     data = {
    #         "username": "testcustomer",
    #         "email": "customer@test.com",
    #         "password": "testpass123",
    #         "user_type": "customer",
    #     }
    #     response = self.client.post(url, data)

    #     self.assertRedirects(response, reverse("customer_profile"))

    def test_login_view_post_invalid_credentials(self):
        url = reverse("login")
        data = {
            "username": "testcompany",
            "email": "company@test.com",
            "password": "wrongpassword",
            "user_type": "company",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid username or password.")

    def test_login_view_post_user_type_mismatch(self):
        url = reverse("login")
        data = {
            "username": "testcompany",
            "email": "company@test.com",
            "password": "testpass123",
            "user_type": "customer",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "User type mismatch.")

    def test_login_view_post_user_not_exist(self):
        url = reverse("login")
        data = {
            "username": "nonexistentuser",
            "email": "nonexistent@test.com",
            "password": "testpass123",
            "user_type": "company",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid username or email.")
