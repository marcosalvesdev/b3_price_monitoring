from django.db import models


class PeriodicTaskAssociation(models.Model):
    periodic_task = models.ForeignKey("django_celery_beat.PeriodicTask", on_delete=models.CASCADE)
    tunnel = models.ForeignKey(
        "PriceTunnel", on_delete=models.CASCADE, related_name="periodic_task_associations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("periodic_task", "tunnel")

    def __str__(self):
        return f"Association of {self.periodic_task.name} with {self.tunnel}"
