from django.db import models


class AssetPrice(models.Model):
    asset = models.ForeignKey("Asset", on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(max_digits=20, decimal_places=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset.ticker} - {self.price} ({self.created_at})"
