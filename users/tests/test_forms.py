from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..forms import UserLoginForm, CompanyRegistrationForm, CustomerRegistrationForm
from ..models import Company

User = get_user_model()

class UserLoginFormTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword",
            is_company=True
        )

    def test_valid_login_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'securepassword',
            'user_type': 'company'
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_username(self):
        form_data = {
            'email': 'testuser@example.com',
            'password': 'securepassword',
            'user_type': 'company'
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['Username  is required.'])

    def test_mismatched_username_email(self):
        form_data = {
            'username': 'testuser',
            'email': 'wrongemail@example.com',
            'password': 'securepassword',
            'user_type': 'company'
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['No user found with this email.'])

    def test_invalid_user_type(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'securepassword',
            'user_type': 'customer'
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['User type mismatch.'])

class CompanyRegistrationFormTests(TestCase):
    
    def test_valid_company_registration(self):
        form = CompanyRegistrationForm(data={
            'email': 'company@example.com',
            'username': 'companyuser',
            'field_of_work': 'Gardening',
            'description': 'A company that provides gardening services.',
            'password': 'password123',
            'password_confirmation': 'password123',
        })
        self.assertTrue(form.is_valid())
        
    def test_invalid_company_registration_email_exists(self):
        # Create a User instance first
        user = User.objects.create_user(username='existinguser', email='company@example.com', password='password123', is_company=True)
        
        # Create Company instance and associate with the User
        Company.objects.create(
            user=user,
            email='company@example.com',
            username='existinguser',
            field_of_work='Gardening',
            description='A company that provides gardening services.'
        )
        
        form = CompanyRegistrationForm(data={
            'email': 'company@example.com',
            'username': 'newuser',
            'field_of_work': 'Gardening',
            'description': 'A new company.',
            'password': 'password123',
            'password_confirmation': 'password123',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This email is already registered.'])
        
    def test_invalid_company_registration_password_mismatch(self):
        form = CompanyRegistrationForm(data={
            'email': 'company@example.com',
            'username': 'companyuser',
            'field_of_work': 'Gardening',
            'description': 'A company.',
            'password': 'password123',
            'password_confirmation': 'password456',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['Passwords do not match.'])
class CustomerRegistrationFormTests(TestCase):
    
    def test_valid_customer_registration(self):
        form = CustomerRegistrationForm(data={
            'username': 'customeruser',
            'email': 'customer@example.com',
            'password': 'password123',
            'password_confirmation': 'password123',
            'date_of_birth': '2000-01-01',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_customer_registration_email_exists(self):
        User.objects.create_user(username='existinguser', email='customer@example.com', password='password123')
        
        form = CustomerRegistrationForm(data={
            'username': 'newuser',
            'email': 'customer@example.com',
            'password': 'password123',
            'password_confirmation': 'password123',
            'date_of_birth': '2000-01-01',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This email is already registered.'])
        
    def test_invalid_customer_registration_password_mismatch(self):
        form = CustomerRegistrationForm(data={
            'username': 'customeruser',
            'email': 'customer@example.com',
            'password': 'password123',
            'password_confirmation': 'password456',
            'date_of_birth': '2000-01-01',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password_confirmation'], ['Passwords do not match.'])