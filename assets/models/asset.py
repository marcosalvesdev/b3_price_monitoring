from django.core.exceptions import ValidationError
from django.db import models

from assets.services.brapi.asset_validator import BrapiApiAssetValidator
from assets.utils.validators.asset_validator import AssetValidator


class AssetChoices(models.TextChoices):
    STOCK = "stock", "Stock"
    CRYPTO = "crypto", "Crypto"
    ETF = "etf", "ETF"


class Asset(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the asset (eg. Vale S.A.)")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    # TODO: Mudar o nome do campo de ticker para symbol e alterar todos os lugares onde ele é
    # referenciado, para ficar mais genérico e não só relacionado a ações.
    ticker = models.CharField(max_length=10, help_text="eg. PETR4, VALE3)")

    type = models.CharField(choices=AssetChoices.choices, max_length=10)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "ticker")

    def __str__(self):
        return self.name

    def clean(self):
        self.assert_validation()
        super().clean()

    def assert_validation(self):
        if self.pk:
            asset = Asset.objects.get(pk=self.pk)
            if asset.ticker == self.ticker and asset.type == self.type:
                return None

        external_validator = BrapiApiAssetValidator(ticker=self.ticker, asset_type=self.type)
        validator = AssetValidator(external_validator=external_validator)

        if not validator.is_valid:
            raise ValidationError(
                "We couldn't validate this asset. "
                "Verify if you inserted the correct ticker to the asset type."
            )

        return None

    def create_asset_price(self, price: float | int):
        from assets.models import AssetPrice

        return AssetPrice.objects.create(asset=self, price=price)
