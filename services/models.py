from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import Company, Customer

User = get_user_model()


class Service(models.Model):
    """
    Model representing a service offered by a company.
    Each service has details like name, description, price, and rating.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0,
        help_text="Service rating from 0-5"
    )

    # Predefined service categories
    choices = (
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
    )
    field = models.CharField(
        max_length=30,
        choices=choices,
        blank=False,
        null=False,
        help_text="Category of service"
    )
    date = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        unique_together = ("name", "company")  # Prevent duplicate service names per company
        indexes = [
            models.Index(fields=['name', 'company']),  # Optimize lookups
            models.Index(fields=['field']),  # Optimize category filtering
        ]

    def __str__(self):
        return self.name


class RequestedService(models.Model):
    """
    Model representing a service request from a customer.
    Tracks request details, status, and customer feedback.
    """
    SERVICE_STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="requested_services"
    )
    service_name = models.CharField(max_length=100)
    service_field = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    service_time_hours = models.DecimalField(max_digits=5, decimal_places=2)
    requested_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=SERVICE_STATUS_CHOICES,
        default="in_progress"
    )
    requested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="requested_services"
    )

    # Customer feedback fields
    customer_review = models.TextField(
        blank=True,
        null=True,
        help_text="Optional customer feedback"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0,
        help_text="Rating given by customer (0-5)"
    )

    class Meta:
        indexes = [
            models.Index(fields=['company', 'service_name']),  # Optimize rating calculations
            models.Index(fields=['status']),  # Optimize status filtering
        ]

    def save(self, *args, **kwargs):
        """
        Override save method to update the associated service's average rating
        whenever a new rating is added or updated.
        """
        super().save(*args, **kwargs)

        # Find and update corresponding service rating
        service = Service.objects.filter(
            name=self.service_name,
            company=self.company
        ).first()

        if not service:
            return

        # Calculate new average rating
        related_requests = RequestedService.objects.filter(
            company=self.company,
            service_name=self.service_name
        )
        request_count = related_requests.count()

        if request_count > 0:
            total_rating = sum(req.rating for req in related_requests)
            service.rating = round(total_rating / request_count)
            service.save(update_fields=['rating'])  # Optimize by only updating rating field

    def __str__(self):
        return f"{self.service_field} - {self.company.username} - {self.status}"
