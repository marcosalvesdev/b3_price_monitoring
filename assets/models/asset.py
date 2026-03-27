from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from assets.services.yfinance.asset_validator import YFinanceAssetValidator
from assets.utils.validators.asset_validator import AssetValidator


class AssetChoices(models.TextChoices):
    STOCK = "stock", "Stock"
    CRYPTO = "crypto", "Crypto"
    ETF = "etf", "ETF"


class Asset(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the asset (eg. Vale S.A.)")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10, help_text="eg. PETR4, VALE3)")
    type = models.CharField(choices=AssetChoices.choices, max_length=10)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "symbol")

    def __str__(self):
        return self.name

    def clean(self):
        self.assert_validation()
        super().clean()

    def assert_validation(self):
        if self.pk:
            asset = Asset.objects.get(pk=self.pk)
            if asset.symbol == self.symbol and asset.type == self.type:
                return None

        external_validator = YFinanceAssetValidator(symbol=self.symbol, asset_type=self.type)
        validator = AssetValidator(external_validator=external_validator)

        if not validator.is_valid:
            raise ValidationError(
                "We couldn't validate this asset. "
                "Verify if you inserted the correct symbol to the asset type."
            )

        return None

    def create_asset_price(self, price: float | int):
        from assets.models import AssetPrice

        return AssetPrice.objects.create(asset=self, price=price)
