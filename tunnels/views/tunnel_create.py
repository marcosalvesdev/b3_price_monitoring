from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.urls import reverse_lazy
from django.views.generic import CreateView

from assets.models import Asset
from tunnels.forms import TunnelCreateForm
from tunnels.models import PriceTunnel


class TunnelCreateView(LoginRequiredMixin, CreateView):
    model = PriceTunnel
    form_class = TunnelCreateForm
    template_name = "tunnels/tunnel_create.html"
    success_url = reverse_lazy("tunnels:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("tunnels:list")
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["asset"].queryset = Asset.objects.filter(user=self.request.user)
        return form

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                return self.form_valid(form)
            except IntegrityError as err:
                # TODO: Find a way to handle this error outside of the view,
                #  maybe in the model validation or in the form validation
                if "unique constraint" in str(err).lower():
                    err = ValidationError(
                        "A tunnel with this combination of asset and price range already exists."
                    )
                form.add_error(field=None, error=err)

                return self.form_invalid(form)
        else:
            return self.form_invalid(form)
