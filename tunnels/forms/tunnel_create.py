import logging

from django import forms

from tunnels.models import PriceTunnel
from tunnels.utils.tasks import task_names
from tunnels.utils.tasks.periodic_tunnel_tasks_manager import PeriodicTunnelTasksManager

logger = logging.getLogger(__name__)


class TunnelCreateForm(forms.ModelForm):
    class Meta:
        model = PriceTunnel
        fields = [
            "asset",
            "upper_limit",
            "lower_limit",
            "check_interval_minutes",
            "is_active",
        ]
        widgets = {"asset": forms.Select()}

    def save(self, **kwargs):
        tunnel = super().save(commit=True)
        try:
            tunnel_tasks_manager = PeriodicTunnelTasksManager()
            tunnel_tasks_manager.create_periodic_task_for_tunnel(
                tunnel=tunnel, task_name=task_names.TUNNEL_ASSET_PRICE_CHECK
            )
        except Exception as e:
            # If task creation fails, we can choose to delete the tunnel or log the error.
            # For now, we'll just log the error and keep the tunnel.
            logger.error(f"Failed to create periodic task for tunnel {tunnel.id}: {e}")
        return tunnel
