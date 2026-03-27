from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from tunnels.forms import IntervalCheckCreateForm
from tunnels.models import PeriodicTaskAssociation, PriceTunnel


class TunnelIntervalCheckCreateView(LoginRequiredMixin, CreateView):
    model = PeriodicTaskAssociation
    form_class = IntervalCheckCreateForm
    template_name = "tunnels/tunnel_interval_check_form.html"
    success_url = reverse_lazy("tunnels:list")

    def get_queryset(self):
        self.queryset = super().get_queryset().filter(tunnel__asset__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("tunnels:list")
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.kwargs.get("pk"):
            queryset = PriceTunnel.objects.filter(
                id=self.kwargs.get("pk"), asset__user=self.request.user
            )
            tunnel = queryset.first()
            form.fields["tunnel"].choices = [(tunnel.id, str(tunnel))]
            form.fields["tunnel"].queryset = queryset
        return form

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as _:
            form.add_error(
                None,
                "An error occurred while creating this interval check. Please try again later or contact support if the problem persists.",  # noqa: E501
            )
            return self.form_invalid(form)
