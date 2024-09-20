from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from services.models import Service
from django.utils import timezone
from decimal import Decimal
from users.models import Company


class HomeViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@test.com", password="password123"
        )

        # Create a test company
        self.company = Company.objects.create(
            user=self.user,
            username="Test Company",
            description="A sample company",
            field_of_work="IT Services",
        )

        # Create sample services
        self.service1 = Service.objects.create(
            name="Service 1",
            description="A sample service",
            price_hour=Decimal("100.00"),
            company=self.company,  # Associate the service with the company
            date=timezone.now(),
        )
        self.service2 = Service.objects.create(
            name="Service 2",
            description="Another sample service",
            price_hour=Decimal("150.00"),
            company=self.company,
            date=timezone.now(),
        )

    def test_home_view_status_code(self):
        url = reverse("main:home")  # Assuming you have a URL name 'home'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        url = reverse("main:home")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "main/home.html")

    def test_home_view_context(self):
        url = reverse("main:home")
        response = self.client.get(url)
        self.assertIn("services", response.context)
        self.assertIn("most_requested_services", response.context)

        # Verify that services are correctly passed in context
        services = response.context["services"]
        self.assertEqual(len(services), 2)
        self.assertEqual(services[0].name, "Service 1")
        self.assertEqual(services[1].name, "Service 2")


class LogoutViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@test.com", password="password123"
        )
        self.client.login(username="testuser", password="password123")

    def test_logout_view_status_code(self):
        url = reverse("main:logout")  # Assuming you have a URL name 'logout'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_logout_view_redirects_when_not_logged_in(self):
        self.client.logout()  # Log the user out
        url = reverse("main:logout")
        response = self.client.get(url)
        expected_url = reverse("users:choose_registration") + "?next=" + url
        self.assertRedirects(response, expected_url)

    def test_logout_view_uses_correct_template(self):
        url = reverse("main:logout")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "main/logout.html")

    def test_logout_functionality(self):
        url = reverse("main:logout")
        response = self.client.get(url)
        self.assertNotIn(
            "_auth_user_id", self.client.session
        )  # Check if user is logged out
