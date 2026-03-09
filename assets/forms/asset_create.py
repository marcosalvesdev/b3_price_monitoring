from django import forms

from assets.models import Asset, AssetChoices


class AssetCreateForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["name", "symbol", "type", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "symbol": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.Select(choices=AssetChoices.choices, attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }
