from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from tunnels.forms import TunnelUpdateForm
from tunnels.models import PriceTunnel


class TunnelUpdateView(LoginRequiredMixin, UpdateView):
    model = PriceTunnel
    form_class = TunnelUpdateForm
    template_name = "tunnels/tunnel_update.html"
    success_url = reverse_lazy("tunnels:list")
    context_object_name = "tunnel"
