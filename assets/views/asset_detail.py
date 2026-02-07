from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from assets.models import Asset


class AssetDetailView(LoginRequiredMixin, DetailView):
    model = Asset
    template_name = 'assets/asset_detail.html'
    context_object_name = 'asset'

    def get_queryset(self):
        return Asset.objects.filter(user=self.request.user)
