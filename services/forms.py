from django import forms
from .models import RequestedService
from users.models import Company


class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label="Description")
    price_hour = forms.DecimalField(decimal_places=2, max_digits=5, min_value=0.00)
    field = forms.ChoiceField(required=True)

    def __init__(self, *args, choices="", **kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        # adding choices to fields
        if choices:
            self.fields["field"].choices = choices
        # adding placeholders to form fields
        self.fields["name"].widget.attrs["placeholder"] = "Enter Service Name"
        self.fields["description"].widget.attrs["placeholder"] = "Enter Description"
        self.fields["price_hour"].widget.attrs["placeholder"] = "Enter Price per Hour"

        self.fields["name"].widget.attrs["autocomplete"] = "off"


class RequestServiceForm(forms.ModelForm):
    class Meta:
        model = RequestedService
        fields = ["address", "service_time_hours"]

        widgets = {
            "address": forms.TextInput(attrs={"placeholder": "Your address"}),
            "service_time_hours": forms.NumberInput(
                attrs={"placeholder": "Service time in hours"}
            ),
        }
