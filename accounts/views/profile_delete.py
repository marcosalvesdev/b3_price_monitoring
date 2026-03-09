from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from accounts.models import User


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "accounts/profile/delete.html"
    success_url = reverse_lazy("accounts:login")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("accounts:profile")
        return context

    def form_valid(self, form):
        logout(self.request)
        return super().form_valid(form)
