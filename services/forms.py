from django import forms
from .models import RequestedService
from users.models import Company


class CreateNewService(forms.Form):
    """
    Form for creating a new service offering.
    Handles service details like name, description, price and category.
    """
    name = forms.CharField(
        max_length=40,
        help_text="Name of the service (max 40 characters)"
    )
    description = forms.CharField(
        widget=forms.Textarea,
        label="Description",
        help_text="Detailed description of the service"
    )
    price_hour = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        min_value=0.00,
        help_text="Hourly rate for the service"
    )
    field = forms.ChoiceField(
        required=True,
        help_text="Category/field of the service"
    )

    def __init__(self, *args, choices="", **kwargs):
        """
        Initialize form with dynamic choices and placeholders.
        Args:
            choices: Service category choices based on company field
        """
        super(CreateNewService, self).__init__(*args, **kwargs)
        
        # Set service category choices if provided
        if choices:
            self.fields["field"].choices = choices

        # Configure field attributes for better UX
        field_attrs = {
            "name": {
                "placeholder": "Enter Service Name",
                "autocomplete": "off"
            },
            "description": {
                "placeholder": "Enter Description"
            },
            "price_hour": {
                "placeholder": "Enter Price per Hour"
            }
        }

        # Apply attributes to form fields
        for field, attrs in field_attrs.items():
            self.fields[field].widget.attrs.update(attrs)


class RequestServiceForm(forms.ModelForm):
    """
    Form for customers to request services.
    Captures service delivery details like address and duration.
    """
    class Meta:
        model = RequestedService
        fields = ["address", "service_time_hours"]

        widgets = {
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Your address",
                    "class": "form-control"
                }
            ),
            "service_time_hours": forms.NumberInput(
                attrs={
                    "placeholder": "Service time in hours",
                    "class": "form-control",
                    "min": "0.5",
                    "step": "0.5"
                }
            ),
        }
