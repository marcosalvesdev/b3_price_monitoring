from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from tunnels.models import PriceTunnel


class TunnelDetailView(LoginRequiredMixin, DetailView):
    model = PriceTunnel
    template_name = "tunnels/tunnel_detail.html"
    context_object_name = "tunnel"

    def get_queryset(self):
        return super().get_queryset().filter(asset__user=self.request.user).select_related("asset")
