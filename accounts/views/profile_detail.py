from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from accounts.models import User


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/profile/detail.html"
    context_object_name = "profile_user"

    def get_object(self):
        return self.request.user
