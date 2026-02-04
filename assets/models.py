from django.core.exceptions import ValidationError
from django.db import models
from assets.utils.validators.asset_validator import AssetValidator


class AssetChoices(models.TextChoices):
    STOCK = "stock", "Stock"
    CRYPTO = "crypto", "Crypto"
    ETF = "etf", "ETF"


class Asset(models.Model):
    name = models.CharField(max_length=255, help_text='Name of the asset (eg. Vale S.A.)')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    ticker = models.CharField(
        max_length=10,
        help_text='eg. PETR4, VALE3)'
    )
    type = models.CharField(choices=AssetChoices.choices, max_length=10)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def assert_validation(self):

        if self.pk:
            asset = Asset.objects.get(pk=self.pk)
            if asset.ticker == self.ticker and asset.type == self.type:
                return None

        asset_validator = AssetValidator(ticker=self.ticker, asset_type=self.type)
        if not asset_validator.is_valid:
            raise ValidationError(
                "We couldn't validate this asset. "
                "Verify if you inserted the correct ticker to the asset type."
            )

    def clean(self):
        self.assert_validation()
        super().clean()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('user', 'ticker')
