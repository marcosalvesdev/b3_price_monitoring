from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from tunnels.models import PriceTunnel


class TunnelDeleteView(LoginRequiredMixin, DeleteView):
    model = PriceTunnel
    template_name = "tunnels/tunnel_delete.html"
    success_url = reverse_lazy("tunnels:list")
    context_object_name = "tunnel"
