from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import Company, Customer
from ..models import Service, RequestedService
from decimal import Decimal

User = get_user_model()


class ServiceModelTest(TestCase):

    def setUp(self):
        # Create a User instance first
        self.user = User.objects.create_user(
            username="company_user", email="test@company.com", password="password123"
        )

        # Then create the Company instance and link it to the user
        self.company = Company.objects.create(
            user=self.user, username="test_company", email="test@company.com"
        )

        # Create a Service instance
        self.service = Service.objects.create(
            company=self.company,
            name="Plumbing",
            description="Fixing pipes and water systems.",
            price_hour=Decimal("20.00"),
            field="Plumbing",
        )

    def test_service_creation(self):
        self.assertEqual(self.service.name, "Plumbing")
        self.assertEqual(self.service.company, self.company)
        self.assertEqual(self.service.price_hour, Decimal("20.00"))
        self.assertEqual(self.service.rating, 0)

    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            Service.objects.create(
                company=self.company,
                name="Plumbing",  # Duplicate name for the same company
                description="Fixing water pipes.",
                price_hour=Decimal("30.00"),
                field="Plumbing",
            )


class RequestedServiceModelTest(TestCase):

    def setUp(self):
        # Create a User instance first
        self.user = User.objects.create_user(
            username="company_user", email="test@company.com", password="password123"
        )

        # Then create the Company instance and link it to the user
        self.company = Company.objects.create(
            user=self.user, username="test_company", email="test@company.com"
        )

        # Create a Service instance
        self.service = Service.objects.create(
            company=self.company,
            name="Plumbing",
            description="Fixing pipes and water systems.",
            price_hour=Decimal("20.00"),
            field="Plumbing",
        )
        self.requested_service = RequestedService.objects.create(
            company=self.company,
            service_name="Plumbing",
            service_field="Plumbing",
            address="1234 Test St",
            service_time_hours=Decimal("2.00"),
            requested_by=self.user,
            status="in_progress",
        )

    def test_requested_service_creation(self):
        self.assertEqual(self.requested_service.service_name, "Plumbing")
        self.assertEqual(self.requested_service.company, self.company)
        self.assertEqual(self.requested_service.requested_by, self.user)
        self.assertEqual(self.requested_service.service_time_hours, Decimal("2.00"))
        self.assertEqual(self.requested_service.status, "in_progress")

    def test_service_rating_update(self):
        # Create another requested service with a rating
        RequestedService.objects.create(
            company=self.company,
            service_name="Plumbing",
            service_field="Plumbing",
            address="1234 Test St",
            service_time_hours=Decimal("3.00"),
            requested_by=self.user,
            status="completed",
            rating=4,
        )

        # Update rating for the service
        self.requested_service.rating = 5
        self.requested_service.save()

        # Check if the service rating is updated correctly
        self.service.refresh_from_db()
        self.assertEqual(self.service.rating, 4)  # Average of 5 and 4

    def test_service_rating_no_zero_division(self):
        # Ensure rating update doesn't divide by zero
        requested_service = RequestedService.objects.create(
            company=self.company,
            service_name="Non-existent",
            service_field="Plumbing",
            address="1234 Test St",
            service_time_hours=Decimal("3.00"),
            requested_by=self.user,
            status="completed",
            rating=0,
        )
        requested_service.save()

        # Ensure the original service's rating does not change
        self.service.refresh_from_db()
        self.assertEqual(self.service.rating, 0)  # Rating should remain unchanged
