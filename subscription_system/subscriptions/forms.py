from django import forms
from django.contrib.auth.models import User
from .models import Subscription, SubscriptionPlan
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import timedelta


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["billing_cycle", "auto_renew", "notes"]
        widgets = {
            "billing_cycle": forms.Select(attrs={"class": "form-control"}),
            "auto_renew": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Any special requirements or notes?",
                }
            ),
        }


class AdminSubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = "__all__"
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
            "amount_paid": forms.NumberInput(attrs={"step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_date"].initial = timezone.now()

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        billing_cycle = cleaned_data.get("billing_cycle")

        if start_date and billing_cycle:
            if billing_cycle == "monthly":
                end_date = start_date + timedelta(days=30)
            elif billing_cycle == "quarterly":
                end_date = start_date + timedelta(days=90)
            else:  # annually
                end_date = start_date + timedelta(days=365)

            cleaned_data["end_date"] = end_date

        return cleaned_data
