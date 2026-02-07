from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from assets.models import Asset


class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = Asset
    template_name = "assets/asset_delete.html"
    success_url = reverse_lazy("assets:list")
