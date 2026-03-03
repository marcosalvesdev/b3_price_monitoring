import json

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from tunnels.models import PeriodicTaskAssociation, PriceTunnel


def tunnel_data(tunnel: PriceTunnel) -> dict:
    """Formats the tunnel data into a dictionary to be used as kwargs for the periodic task."""
    return {
        "tunnel_id": tunnel.id,
        "tunnel_upper_limit": float(tunnel.upper_limit),
        "tunnel_lower_limit": float(tunnel.lower_limit),
        "tunnel_is_active": tunnel.is_active,
        "asset_id": tunnel.asset_id,
        "asset_name": tunnel.asset.name,
        "asset_ticker": tunnel.asset.ticker,
        "asset_type": tunnel.asset.type,
        "asset_is_active": tunnel.asset.is_active,
    }


class PeriodicTunnelTasksManager:
    """Manages the periodic tasks for tunnels."""

    @staticmethod
    def create_periodic_task_for_tunnel(
        tunnel: PriceTunnel, task_name: str, task_args: list = None, task_kwargs: dict = None
    ):
        """
        Creates a periodic task for the given tunnel and task
        Args:
            tunnel (PriceTunnel): The tunnel for which to create the periodic task
            task_name (str): The name of the task to execute periodically. For example, "tunnels.tasks.check_tunnel"
            task_args (list, optional): A list of positional arguments to pass to the task. Defaults to None.
            task_kwargs (dict, optional): A dictionary of keyword arguments to pass to the task. Defaults to None.
        """  # noqa: E501

        task_args = task_args or []
        task_kwargs = task_kwargs or {}

        task_kwargs.update(**tunnel_data(tunnel))

        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=tunnel.check_interval_minutes, period=IntervalSchedule.MINUTES
        )
        periodic_task = PeriodicTask.objects.create(
            interval=schedule,
            name=f"Check Tunnel {tunnel.id} for {tunnel.asset.name}",
            task=task_name,
            args=json.dumps(task_args),
            kwargs=json.dumps(task_kwargs),
        )
        PeriodicTaskAssociation.objects.create(tunnel=tunnel, periodic_task=periodic_task)

    @staticmethod
    def delete_periodic_task_for_tunnel(tunnel: PriceTunnel):
        """Deletes the periodic task associated with the given tunnel."""
        periodic_task_ids = PeriodicTaskAssociation.objects.filter(tunnel=tunnel).values_list(
            "periodic_task_id"
        )

        if not periodic_task_ids:
            return None

        periodic_tasks = PeriodicTask.objects.filter(id__in=periodic_task_ids)
        periodic_tasks.delete()
        return None
