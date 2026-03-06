from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.urls import reverse_lazy


class UserPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password/change/change.html"
    success_url = reverse_lazy("accounts:password_change_done")


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "accounts/password/change/done.html"
