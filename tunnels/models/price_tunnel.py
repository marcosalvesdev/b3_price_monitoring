from django.core.exceptions import ValidationError
from django.db import models

from tunnels.utils.validators.tunnel_validator import TunnelValidator


class PriceTunnel(models.Model):
    asset = models.ForeignKey("assets.Asset", on_delete=models.CASCADE, related_name="tunnels")
    upper_limit = models.DecimalField(max_digits=10, decimal_places=2)
    lower_limit = models.DecimalField(max_digits=10, decimal_places=2)
    check_interval_minutes = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("asset", "lower_limit", "upper_limit")

    def __str__(self):
        return f"Tunnel of {self.asset.name} from {self.lower_limit} to {self.upper_limit}"

    def clean(self):
        validator = TunnelValidator(
            lower_limit=self.lower_limit,
            upper_limit=self.upper_limit,
            interval=self.check_interval_minutes,
        )

        if not validator.limits_are_valid:
            raise ValidationError("Lower limit must be less than upper limit.")

        if not validator.interval_is_valid:
            raise ValidationError("Check interval must be greater than zero.")

    def ready_to_check(self):
        if not (self.is_active and self.asset.is_active):
            raise ValidationError("Tunnel or asset is not active.")

    def asset_price_is_above_upper_limit(self, price: float | int):
        return price > self.upper_limit

    def asset_price_is_below_lower_limit(self, price: float | int):
        return price < self.lower_limit
