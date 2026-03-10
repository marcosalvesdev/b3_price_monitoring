from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView

from tunnels.models import PriceTunnel


class TunnelDeleteView(LoginRequiredMixin, DeleteView):
    model = PriceTunnel
    template_name = "tunnels/tunnel_delete.html"
    success_url = reverse_lazy("tunnels:list")
    context_object_name = "tunnel"

    def get_queryset(self):
        return super().get_queryset().filter(asset__user=self.request.user).select_related("asset")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse("tunnels:detail", kwargs={"pk": self.object.pk})
        return context
