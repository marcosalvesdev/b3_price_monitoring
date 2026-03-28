from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from assets.models.asset_price import AssetPrice
from assets.utils.validators.asset_validator import AssetValidator
from assets.utils.validators.base_asset_validator import BaseAssetValidator
from assets.utils.validators.symbol_format_validator import SymbolFormatValidator


class AssetChoices(models.TextChoices):
    STOCK = "stock", "Ação"
    FII = "fii", "FII"
    ETF = "etf", "ETF"
    BDR = "bdr", "BDR"
    CRYPTO = "crypto", "Cripto"


class Asset(models.Model):
    name = models.CharField(
        max_length=255,
        help_text="Full name of the asset (e.g. Petróleo Brasileiro S.A.)",
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    symbol = models.CharField(
        max_length=10,
        help_text="B3 ticker or crypto symbol — always uppercase (e.g. PETR4, BOVA11, BTC).",
    )
    type = models.CharField(choices=AssetChoices.choices, max_length=10)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Default external validator — can be overridden at class or instance level
    # without modifying this module (DIP / Strategy pattern).
    validator_class = None

    class Meta:
        unique_together = ("user", "symbol")

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    def save(self, *args, **kwargs):
        self.symbol = self.symbol.upper()
        super().save(*args, **kwargs)

    def clean(self):
        self.symbol = self.symbol.upper()
        SymbolFormatValidator(symbol=self.symbol, asset_type=self.type).validate()
        self.assert_validation()
        super().clean()

    def assert_validation(self, external_validator: BaseAssetValidator = None):
        if self.pk:
            original = type(self).objects.filter(pk=self.pk).values("symbol", "type").first()
            if original and original["symbol"] == self.symbol and original["type"] == self.type:
                return None

        if external_validator is None:
            if self.validator_class is None:
                from assets.services.yfinance.asset_validator import YFinanceAssetValidator

                self.validator_class = YFinanceAssetValidator
            external_validator = self.validator_class(symbol=self.symbol, asset_type=self.type)

        validator = AssetValidator(external_validator=external_validator)

        if not validator.is_valid:
            raise ValidationError(
                "We couldn't validate this asset. "
                "Verify if you inserted the correct symbol for the selected asset type."
            )

        return None

    def create_asset_price(self, price: float | int):
        return AssetPrice.objects.create(asset=self, price=price)
