from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from assets.models import Asset


class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = Asset
    template_name = "assets/asset_delete.html"
    success_url = reverse_lazy("assets:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("assets:detail", kwargs={"pk": self.object.pk})
        return context
