from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from accounts.forms import ProfileUpdateForm
from accounts.models import User


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "accounts/profile/update.html"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("accounts:profile")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        avatar = self.request.FILES.get("avatar")
        clear_avatar = self.request.POST.get("avatar-clear")
        profile = self.object.profile

        if clear_avatar:
            profile.avatar = None
            profile.save()
        elif avatar:
            profile.avatar = avatar
            profile.save()

        messages.success(self.request, "Profile updated successfully.")
        return response
