from django import forms
from tunnels.models import PriceTunnel


class TunnelUpdateForm(forms.ModelForm):
    class Meta:
        model = PriceTunnel
        fields = ['upper_limit', 'lower_limit', 'check_interval_minutes', 'is_active']
