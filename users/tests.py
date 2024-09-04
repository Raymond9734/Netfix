from django.forms import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Company, Customer
from users.forms import CompanyRegistrationForm, CustomerRegistrationForm, UserLoginForm
from datetime import date

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
        self.assertFalse(
            Company.objects.filter(email="testcompany@example.com").exists()
        )

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
        self.assertFalse(
            Company.objects.filter(email="testcompany@example.com").exists()
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


class CustomerRegistrationFormTests(TestCase):

    def test_form_valid_data(self):
        # Prepare valid form data
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "password_confirmation": "testpassword123",
            "date_of_birth": "2000-01-01",
        }

        # Initialize the form with data
        form = CustomerRegistrationForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Check that the cleaned data is correct
        self.assertEqual(form.cleaned_data["username"], "testuser")
        self.assertEqual(form.cleaned_data["email"], "testuser@example.com")

    def test_form_password_mismatch(self):
        # Prepare form data with mismatched passwords
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "password_confirmation": "wrongpassword",
            "date_of_birth": "2000-01-01",
        }

        # Initialize the form with data
        form = CustomerRegistrationForm(data=form_data)

        # Check that the form is invalid
        self.assertFalse(form.is_valid())

        # Check that the password_confirmation error is present
        self.assertIn("password_confirmation", form.errors)
        self.assertEqual(
            form.errors["password_confirmation"], ["Passwords do not match."]
        )

    def test_form_email_already_registered(self):
        # Create an existing user with the same email
        User.objects.create_user(
            username="existinguser",
            email="testuser@example.com",
            password="testpassword123",
        )

        # Prepare form data with the same email
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "password_confirmation": "testpassword123",
            "date_of_birth": "2000-01-01",
        }

        # Initialize the form with data
        form = CustomerRegistrationForm(data=form_data)

        # Check that the form is invalid
        self.assertFalse(form.is_valid())

        # Check that the email error is present
        self.assertIn("email", form.errors)
        self.assertEqual(form.errors["email"], ["This email is already registered."])

    def test_form_missing_date_of_birth(self):
        # Prepare form data without the date of birth
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "password_confirmation": "testpassword123",
            # 'date_of_birth' is omitted here
        }

        # Initialize the form with data
        form = CustomerRegistrationForm(data=form_data)

        # Check that the form is invalid because date_of_birth is required in the view
        self.assertFalse(form.is_valid())


class UserLoginFormTests(TestCase):

    def test_form_valid_data(self):
        # Prepare valid form data
        form_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
        }

        # Initialize the form with data
        form = UserLoginForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Check that the cleaned data is correct
        self.assertEqual(form.cleaned_data["email"], "testuser@example.com")
        self.assertEqual(form.cleaned_data["password"], "testpassword123")

    def test_form_invalid_email(self):
        # Prepare form data with an invalid email
        form_data = {
            "email": "invalidemail",  # Invalid email format
            "password": "testpassword123",
        }

        # Initialize the form with data
        form = UserLoginForm(data=form_data)

        # Check that the form is invalid
        self.assertFalse(form.is_valid())

        # Check that the email field has errors
        self.assertIn("email", form.errors)

    def test_form_missing_password(self):
        # Prepare form data without a password
        form_data = {
            "email": "testuser@example.com",
            # 'password' is omitted
        }

        # Initialize the form with data
        form = UserLoginForm(data=form_data)

        # Check that the form is invalid
        self.assertFalse(form.is_valid())

        # Check that the password field has errors
        self.assertIn("password", form.errors)

    def test_form_autocomplete_off(self):
        # Prepare valid form data
        form_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
        }

        # Initialize the form with data
        form = UserLoginForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Check if the email field has autocomplete set to "off"
        self.assertEqual(form.fields["email"].widget.attrs["autocomplete"], "off")


class CompanyRegistrationFormTests(TestCase):

    def test_form_valid_data(self):
        # Prepare valid form data
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "password_confirmation": "testpassword123",
            "field_of_work": "Electricity",
        }

        # Initialize the form with data
        form = CompanyRegistrationForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

    def test_form_password_mismatch(self):
        # Prepare form data with mismatched passwords
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "password_confirmation": "wrongpassword",
            "field_of_work": "Electricity",
        }

        # Initialize the form with data
        form = CompanyRegistrationForm(data=form_data)

        # Check that the form is invalid
        self.assertFalse(form.is_valid())

        # Check that the form has errors and contains the correct message
        self.assertIn("__all__", form.errors)
        self.assertEqual(form.errors["__all__"], ["Passwords do not match."])

    def test_form_duplicate_email(self):
        # Create a user with the same email
        User.objects.create_user(
            username="existinguser",
            email="testuser@example.com",
            password="testpassword123",
        )

        # Prepare form data with a duplicate email
        form_data = {
            "username": "newuser",
            "email": "testuser@example.com",
            "password": "newpassword123",
            "password_confirmation": "newpassword123",
            "field_of_work": "Electricity",
        }

        # Initialize the form with data
        form = CompanyRegistrationForm(data=form_data)

        # Check that the form is invalid
        self.assertFalse(form.is_valid())

        # Check that the email field has errors
        self.assertIn("email", form.errors)
        self.assertEqual(form.errors["email"], ["This email is already registered."])

    def test_form_missing_field_of_work(self):
        # Prepare form data without field of work
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "password_confirmation": "testpassword123",
            # 'field_of_work' is omitted
        }

        # Initialize the form with data
        form = CompanyRegistrationForm(data=form_data)

        # Check that the form is invalid
        self.assertFalse(form.is_valid())

        # Check that the field_of_work field has errors
        self.assertIn("field_of_work", form.errors)

    def test_form_field_choices(self):
        # Prepare valid form data
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "password_confirmation": "testpassword123",
            "field_of_work": "Gardening",
        }

        # Initialize the form with data
        form = CompanyRegistrationForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Check if the field_of_work has the correct value
        self.assertEqual(form.cleaned_data["field_of_work"], "Gardening")


class UserModelTests(TestCase):

    def test_user_creation(self):
        # Create a User instance
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
        )

        # Check that the user is created
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")

    def test_user_is_company_field(self):
        # Create a User instance with is_company set to True
        user = User.objects.create_user(
            username="companyuser",
            email="companyuser@example.com",
            password="testpassword123",
            is_company=True,
        )

        # Check that the is_company field is set correctly
        self.assertTrue(user.is_company)

    def test_user_is_customer_field(self):
        # Create a User instance with is_customer set to True
        user = User.objects.create_user(
            username="customeruser",
            email="customeruser@example.com",
            password="testpassword123",
            is_customer=True,
        )

        # Check that the is_customer field is set correctly
        self.assertTrue(user.is_customer)


class CustomerModelTests(TestCase):

    def test_customer_creation(self):
        # Create a User instance
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
        )

        # Create a Customer instance associated with the user
        customer = Customer.objects.create(user=user, date_of_birth=date(2000, 1, 1))

        # Check that the customer is created
        self.assertEqual(customer.user, user)
        self.assertEqual(customer.date_of_birth, date(2000, 1, 1))

    def test_customer_str(self):
        # Create a User instance
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
        )

        # Create a Customer instance associated with the user
        customer = Customer.objects.create(user=user, date_of_birth=date(2000, 1, 1))

        # Check the string representation of the Customer
        self.assertEqual(str(customer), "testuser")


class CompanyModelTests(TestCase):

    def test_company_creation(self):
        # Create a User instance
        user = User.objects.create_user(
            username="companyuser",
            email="companyuser@example.com",
            password="testpassword123",
            is_company=True,
        )

        # Create a Company instance associated with the user
        company = Company.objects.create(
            user=user,
            email="companyuser@example.com",
            username="companyuser",
            field_of_work="Electricity",
            rating=4,
        )

        # Check that the company is created
        self.assertEqual(company.user, user)
        self.assertEqual(company.email, "companyuser@example.com")
        self.assertEqual(company.username, "companyuser")
        self.assertEqual(company.field_of_work, "Electricity")
        self.assertEqual(company.rating, 4)

    def test_company_str(self):
        # Create a User instance
        user = User.objects.create_user(
            username="companyuser",
            email="companyuser@example.com",
            password="testpassword123",
            is_company=True,
        )

        # Create a Company instance associated with the user
        company = Company.objects.create(
            user=user,
            email="companyuser@example.com",
            username="companyuser",
            field_of_work="Electricity",
            rating=4,
        )

        # Check the string representation of the Company
        self.assertEqual(str(company), f"{user.id} - {user.username}")

    def test_company_email_unique(self):
        # Create a User instance
        user1 = User.objects.create_user(
            username="companyuser1",
            email="companyuser@example.com",
            password="testpassword123",
            is_company=True,
        )

        # Create a Company instance with the same email
        Company.objects.create(
            user=user1,
            email="companyuser@example.com",
            username="companyuser1",
            field_of_work="Electricity",
        )

        # Attempt to create another Company instance with the same email, expecting a validation error
        with self.assertRaises(ValidationError):
            user2 = User.objects.create_user(
                username="companyuser2",
                email="companyuser2@example.com",
                password="testpassword123",
                is_company=True,
            )
            company = Company(
                user=user2,
                email="companyuser@example.com",
                username="companyuser2",
                field_of_work="Gardening",
            )
            company.full_clean()  # This should raise a ValidationError due to email uniqueness constraint
