from django import forms

from tunnels.models import PriceTunnel


class TunnelCreateForm(forms.ModelForm):
    class Meta:
        model = PriceTunnel
        fields = [
            "asset",
            "upper_limit",
            "lower_limit",
            "check_interval_minutes",
            "is_active",
        ]
        widgets = {"asset": forms.Select()}
