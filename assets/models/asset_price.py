from django.db import models


class AssetPrice(models.Model):
    asset = models.ForeignKey("Asset", on_delete=models.CASCADE, related_name="prices")
    # max_digits=18, decimal_places=8: handles BRL prices from R$0.00000001
    # (micro-cap crypto) up to R$9,999,999,999.99999999, covering all current
    # and foreseeable B3 and crypto prices.
    price = models.DecimalField(max_digits=18, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset.symbol} — R$ {self.price} ({self.created_at:%d/%m/%Y %H:%M})"
