from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from assets.forms import AssetForm


class AssetCreateView(LoginRequiredMixin, CreateView):
    form_class = AssetForm
    template_name = "assets/asset_create.html"
    success_url = reverse_lazy("assets:list")
    object = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("assets:list")
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
