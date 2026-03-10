from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from tunnels.models import PriceTunnel


class TunnelListView(LoginRequiredMixin, ListView):
    model = PriceTunnel
    template_name = "tunnels/tunnel_list.html"
    context_object_name = "tunnels"

    def get_queryset(self):
        return super().get_queryset().filter(asset__user=self.request.user).select_related("asset")
