from django import forms

from assets.models import Asset, AssetChoices


class AssetForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Asset
        fields = ["name", "symbol", "type", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Petróleo Brasileiro S.A.",
                }
            ),
            "symbol": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. PETR4, BOVA11, BTC",
                }
            ),
            "type": forms.Select(
                choices=AssetChoices.choices,
                attrs={"class": "form-select"},
            ),
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }

    def clean_symbol(self):
        # Always uppercase — B3 tickers and crypto symbols are always uppercase.
        # This also ensures the duplicate-symbol check is case-insensitive.
        symbol = self.cleaned_data.get("symbol", "").upper()
        if symbol and self.user:
            qs = Asset.objects.filter(user=self.user, symbol=symbol)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("An asset with this symbol already exists.")
        return symbol
