from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from assets.models import Asset
from assets.forms import AssetUpdateForm
from django.urls import reverse_lazy


class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    form_class = AssetUpdateForm
    template_name = "assets/asset_update.html"
    success_url = reverse_lazy("assets:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
