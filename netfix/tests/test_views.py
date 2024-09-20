from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import Customer, Company
from services.models import Service, RequestedService
from decimal import Decimal
from django.contrib.auth.models import User


class CustomerProfileViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username="testcustomer", email="customer@test.com", password="password123"
        )
        self.customer = Customer.objects.create(
            user=self.user,
            date_of_birth="1990-01-01",
        )
        self.client.login(username="testcustomer", password="password123")

        # Create a service and requested service for the test user
        self.company = Company.objects.create(
            user=self.user, username="Test Company", email="company@test.com"
        )
        self.service = Service.objects.create(
            company=self.company,
            name="Test Service",
            description="A sample service",
            price_hour=Decimal("100.00"),
            field="Carpentry",
        )
        self.requested_service = RequestedService.objects.create(
            company=self.company,
            requested_by=self.user,
            service_name=self.service.name,
            service_time_hours=2,
            address="123 Test St.",
            requested_at=timezone.now(),
        )

    def test_customer_profile_view_status_code(self):
        url = reverse("customer_profile", kwargs={"name": self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_customer_profile_view_uses_correct_template(self):
        url = reverse("customer_profile", kwargs={"name": self.user.username})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "users/customer_profile.html")

    def test_customer_profile_view_context(self):
        url = reverse("customer_profile", kwargs={"name": self.user.username})
        response = self.client.get(url)
        self.assertIn("user", response.context)
        self.assertIn("customer", response.context)
        self.assertIn("services_with_cost", response.context)
        self.assertIn("age", response.context)

        # Check that the service request has the correct total cost
        services_with_cost = response.context["services_with_cost"]
        self.assertEqual(len(services_with_cost), 1)
        self.assertEqual(services_with_cost[0]["total_cost"], Decimal("200.00"))

    def test_customer_age_calculation(self):
        url = reverse("customer_profile", kwargs={"name": self.user.username})
        response = self.client.get(url)
        age = response.context["age"]
        self.assertEqual(age, timezone.now().year - 1990)


class CompanyProfileViewTest(TestCase):
    def setUp(self):
        # Create a test company user
        self.user = get_user_model().objects.create_user(
            username="testcompany", email="company@test.com", password="password123"
        )
        self.company = Company.objects.create(
            user=self.user, username="Test Company", email="company@test.com"
        )
        self.client.login(username="testcompany", password="password123")

        # Create a service for the company
        self.service = Service.objects.create(
            company=self.company,
            name="Company Service",
            description="A company service",
            price_hour=Decimal("150.00"),
            field="Carpentry",
            date=timezone.now(),
        )

    def test_company_profile_view_status_code(self):
        url = reverse("company_profile", kwargs={"name": self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_company_profile_view_uses_correct_template(self):
        url = reverse("company_profile", kwargs={"name": self.user.username})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "users/profile.html")

    def test_company_profile_view_context(self):
        url = reverse("company_profile", kwargs={"name": self.user.username})
        response = self.client.get(url)
        self.assertIn("user", response.context)
        self.assertIn("services", response.context)
        self.assertIn("reviews", response.context)

        # Check that the company services are correct
        services = response.context["services"]
        self.assertEqual(len(services), 1)
        self.assertEqual(services[0].name, "Company Service")
