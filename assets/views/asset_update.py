from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from assets.forms import AssetUpdateForm
from assets.models import Asset


class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    form_class = AssetUpdateForm
    template_name = "assets/asset_update.html"
    success_url = reverse_lazy("assets:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("assets:detail", kwargs={"pk": self.object.pk})
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
