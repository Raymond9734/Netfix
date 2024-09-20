from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.contrib.auth import get_user_model
from ..forms import CreateNewService, RequestServiceForm
from ..models import Service, RequestedService
from users.models import Company, Customer

User = get_user_model()


class CreateNewServiceFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.company = Company.objects.create(username="test_company", user=self.user)
        self.choices = [
            ("Air Conditioner", "Air Conditioner"),
            ("Carpentry", "Carpentry"),
            ("Electricity", "Electricity"),
            ("Gardening", "Gardening"),
            ("Home Machines", "Home Machines"),
            ("House Keeping", "House Keeping"),
            ("Interior Design", "Interior Design"),
            ("Locks", "Locks"),
            ("Painting", "Painting"),
            ("Plumbing", "Plumbing"),
            ("Water Heaters", "Water Heaters"),
        ]
        self.form_data = {
            "name": "Test Service",
            "description": "This is a test service",
            "price_hour": "10.50",
            "field": "Carpentry",
        }

    def test_valid_form(self):
        form = CreateNewService(data=self.form_data, choices=self.choices)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test with empty data
        form = CreateNewService(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_invalid_choice(self):
        invalid_data = self.form_data.copy()
        invalid_data["field"] = "InvalidChoice"
        form = CreateNewService(data=invalid_data, choices=self.choices)
        self.assertFalse(form.is_valid())
        self.assertIn("field", form.errors)

    def test_name_max_length(self):
        self.form_data["name"] = (
            "A" * 41
        )  # 41 characters, which is more than max_length
        form = CreateNewService(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_price_hour_min_value(self):
        self.form_data["price_hour"] = "-1.00"
        form = CreateNewService(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("price_hour", form.errors)

    def test_widget_attributes(self):
        form = CreateNewService()
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"], "Enter Service Name"
        )
        self.assertEqual(
            form.fields["description"].widget.attrs["placeholder"], "Enter Description"
        )
        self.assertEqual(
            form.fields["price_hour"].widget.attrs["placeholder"],
            "Enter Price per Hour",
        )
        self.assertEqual(form.fields["name"].widget.attrs["autocomplete"], "off")


class RequestServiceFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.company = Company.objects.create(username="test_company", user=self.user)
        self.service = Service.objects.create(
            company=self.company,
            name="Test Service",
            description="Test Description",
            price_hour=10.00,
            field="Air Conditioner",
        )
        self.form_data = {"address": "123 Test St", "service_time_hours": 2}

    def test_valid_form(self):
        form = RequestServiceForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test with empty data
        form = RequestServiceForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_widget_attributes(self):
        form = RequestServiceForm()
        self.assertEqual(
            form.fields["address"].widget.attrs["placeholder"], "Your address"
        )
        self.assertEqual(
            form.fields["service_time_hours"].widget.attrs["placeholder"],
            "Service time in hours",
        )

    def test_model_form_save(self):
        form = RequestServiceForm(data=self.form_data)
        self.assertTrue(form.is_valid())

        # Save the form without committing to the database
        instance = form.save(commit=False)
        instance.company = self.company
        instance.service_name = self.service.name
        instance.service_field = self.service.field
        instance.requested_by = self.user
        instance.save()

        # Check if the instance was saved correctly
        saved_instance = RequestedService.objects.get(id=instance.id)
        self.assertEqual(saved_instance.address, "123 Test St")
        self.assertEqual(saved_instance.service_time_hours, 2)
        self.assertEqual(saved_instance.company, self.company)
        self.assertEqual(saved_instance.service_name, "Test Service")
        self.assertEqual(saved_instance.service_field, "Air Conditioner")
        self.assertEqual(saved_instance.requested_by, self.user)
        self.assertEqual(saved_instance.status, "in_progress")

    def test_rating_update(self):
        # Create a requested service
        requested_service = RequestedService.objects.create(
            company=self.company,
            service_name=self.service.name,
            service_field=self.service.field,
            address="123 Test St",
            service_time_hours=2,
            requested_by=self.user,
            rating=4,
        )

        # Check if the service rating is updated
        self.service.refresh_from_db()
        self.assertEqual(self.service.rating, 4)

        # Create another requested service with a different rating
        RequestedService.objects.create(
            company=self.company,
            service_name=self.service.name,
            service_field=self.service.field,
            address="456 Test Ave",
            service_time_hours=3,
            requested_by=self.user,
            rating=2,
        )

        # Check if the service rating is updated to the new average
        self.service.refresh_from_db()
        self.assertEqual(self.service.rating, 3)  # (4 + 2) / 2 = 3
