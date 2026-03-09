from django import forms

from tunnels.models import PriceTunnel


class TunnelUpdateForm(forms.ModelForm):
    class Meta:
        model = PriceTunnel
        fields = ["upper_limit", "lower_limit", "check_interval_minutes", "is_active"]
        widgets = {
            "upper_limit": forms.NumberInput(attrs={"class": "form-control font-monospace"}),
            "lower_limit": forms.NumberInput(attrs={"class": "form-control font-monospace"}),
            "check_interval_minutes": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        required_fields = ["upper_limit", "lower_limit", "check_interval_minutes"]
