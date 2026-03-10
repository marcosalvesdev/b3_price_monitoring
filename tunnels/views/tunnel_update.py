from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

from tunnels.forms import TunnelUpdateForm
from tunnels.models import PriceTunnel


class TunnelUpdateView(LoginRequiredMixin, UpdateView):
    model = PriceTunnel
    form_class = TunnelUpdateForm
    template_name = "tunnels/tunnel_update.html"
    success_url = reverse_lazy("tunnels:list")
    context_object_name = "tunnel"

    def get_queryset(self):
        return super().get_queryset().filter(asset__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse("tunnels:detail", kwargs={"pk": self.object.pk})
        return context
