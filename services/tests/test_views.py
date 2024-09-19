import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Company
from ..models import Service, RequestedService
from django.utils import timezone

User = get_user_model()


class ServiceViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a company user and log them in
        self.company_user = User.objects.create_user(
            username="companyuser", password="password", is_company=True
        )
        self.company = Company.objects.create(
            user=self.company_user, username="companyuser", field_of_work="IT"
        )

        # Create a customer user
        self.customer_user = User.objects.create_user(
            username="customeruser", password="password", is_customer=True
        )

        # Create a service
        self.service = Service.objects.create(
            company=self.company,
            name="Service 1",
            description="Service description",
            price_hour=50,
            field="IT",
            date=timezone.now(),
        )

    def test_index_view(self):
        # Test service index view
        self.client.login(username="companyuser", password="password")
        response = self.client.get(
            reverse("services:service_detail", args=[self.service.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/single_service.html")

    def test_create_view_get(self):
        # Test GET request for create service view
        self.client.login(username="companyuser", password="password")
        response = self.client.get(reverse("services:services_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/create_service.html")

    def test_create_view_post(self):
        # Test POST request for create service
        self.client.login(username="companyuser", password="password")
        post_data = {
            "name": "New Service",
            "description": "New service description",
            "price_hour": 100,
            "field": "IT",
        }
        response = self.client.post(reverse("services:services_create"), post_data)
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful creation
        self.assertTrue(Service.objects.filter(name="New Service").exists())

    def test_request_service_view_get(self):
        # Test GET request for requesting a service
        self.client.login(username="customeruser", password="password")
        response = self.client.get(
            reverse(
                "services:request_service",
                args=[self.company.username, self.service.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/request_service.html")

    def test_request_service_view_post(self):
        # Test POST request for requesting a service
        self.client.login(username="customeruser", password="password")
        post_data = {
            "address": "123 Street",
            "service_time_hours": 5,
        }
        response = self.client.post(
            reverse(
                "services:request_service",
                args=[self.company.username, self.service.id],
            ),
            post_data,
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful request
        self.assertTrue(
            RequestedService.objects.filter(
                company=self.company, service_name=self.service
            ).exists()
        )

    def test_services_list_view(self):
        # Test services list view
        self.client.login(username="customeruser", password="password")
        response = self.client.get(reverse("services:service_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "service_main.html")

    def test_service_by_category_view(self):
        # Test service by category view
        self.client.login(username="customeruser", password="password")
        response = self.client.get(reverse("services:service_by_category"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/service_by_category.html")

    def test_most_requested_services_view(self):
        # Test most requested services view
        RequestedService.objects.create(
            company=self.company,
            service_name=self.service,
            service_field=self.service.field,
            service_time_hours=3,
            requested_by=self.customer_user,
        )
        self.client.login(username="customeruser", password="password")
        response = self.client.get(reverse("services:most_requested_services"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/most_requested_services.html")

    def test_submit_review_view(self):
        # Test submit review view with POST
        requested_service = RequestedService.objects.create(
            company=self.company,
            service_name=self.service,
            service_field=self.service.field,
            service_time_hours=3,
            requested_by=self.customer_user,
        )
        self.client.login(username="customeruser", password="password")
        post_data = json.dumps(
            {"review": "Great service!", "rating": 5, "status": "completed"}
        )
        response = self.client.post(
            reverse("submit-review", args=[requested_service.id]),
            post_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        requested_service.refresh_from_db()
        self.assertEqual(requested_service.customer_review, "Great service!")
        self.assertEqual(requested_service.rating, 5)
        self.assertEqual(requested_service.status, "completed")

    def test_mark_service_complete_view(self):
        # Test marking a service as complete
        requested_service = RequestedService.objects.create(
            company=self.company,
            service_name=self.service,
            service_field=self.service.field,
            requested_by=self.customer_user,
            service_time_hours=3,
            status="in_progress",
        )
        self.client.login(username="customeruser", password="password")
        response = self.client.post(
            reverse("mark-service-complete", args=[requested_service.id])
        )
        self.assertEqual(response.status_code, 200)
        requested_service.refresh_from_db()
        self.assertEqual(requested_service.status, "completed")
