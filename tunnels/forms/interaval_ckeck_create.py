from django import forms
from django.core.exceptions import ValidationError

from tunnels.models import PeriodicTaskAssociation
from tunnels.utils.tasks import task_names
from tunnels.utils.tasks.periodic_tunnel_tasks_manager import (
    PeriodicTunnelTasksManager as periodic_tasks_manager,
)


class IntervalCheckCreateForm(forms.ModelForm):
    check_interval_minutes = forms.IntegerField(
        label="Check Interval (minutes)",
        min_value=1,
        help_text="Enter the interval in minutes for checking the tunnel conditions.",
    )

    class Meta:
        model = PeriodicTaskAssociation
        fields = ["tunnel", "check_interval_minutes"]
        widgets = {
            "tunnel": forms.Select(attrs={"class": "form-control"}),
            "check_interval_minutes": forms.NumberInput(
                attrs={"class": "form-control font-monospace"}
            ),
        }

    def clean_tunnel(self):
        tunnel = self.cleaned_data.get("tunnel")
        if not tunnel:
            raise ValidationError("Tunnel not found to create this interval check.")

        existing_tasks = tunnel.periodic_task_associations.filter(tunnel=tunnel)
        if existing_tasks.exists():
            raise ValidationError(
                "A check interval already exists for this tunnel. Please update the existing task instead of creating a new one."  # noqa: E501
            )

        return tunnel

    def save(self, commit=True):
        instance = super().save(commit=False)
        tunnel = instance.tunnel

        tunnel.check_interval_minutes = self.cleaned_data["check_interval_minutes"]

        instance.tunnel = tunnel
        periodic_task, _ = periodic_tasks_manager.create_periodic_task_for_tunnel(
            tunnel=tunnel,
            task_name=task_names.TUNNEL_ASSET_PRICE_CHECK,
        )
        instance.periodic_task = periodic_task

        if commit:
            tunnel.save()
            instance.save()

        return instance
