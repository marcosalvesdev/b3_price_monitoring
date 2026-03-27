import logging

from django import forms

from tunnels.models import PriceTunnel

logger = logging.getLogger(__name__)


class TunnelCreateForm(forms.ModelForm):
    class Meta:
        model = PriceTunnel
        fields = [
            "asset",
            "upper_limit",
            "lower_limit",
            "is_active",
        ]
        widgets = {
            "asset": forms.Select(attrs={"class": "form-select"}),
            "upper_limit": forms.NumberInput(attrs={"class": "form-control font-monospace"}),
            "lower_limit": forms.NumberInput(attrs={"class": "form-control font-monospace"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
