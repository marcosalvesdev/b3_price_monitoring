from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from tunnels.models import PriceTunnel


class TunnelDetailView(LoginRequiredMixin, DetailView):
    model = PriceTunnel
    template_name = 'tunnels/tunnel_detail.html'
    context_object_name = 'tunnel'

    def get_queryset(self):
        return PriceTunnel.objects.filter(asset__user=self.request.user)
