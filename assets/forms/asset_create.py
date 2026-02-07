
from django import forms

from assets.models import Asset, AssetChoices


class AssetCreateForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'ticker', 'type', 'description']
        widgets = {
            'type': forms.Select(choices=AssetChoices.choices),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
