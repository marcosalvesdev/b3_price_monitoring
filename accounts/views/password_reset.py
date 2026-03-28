from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import reverse_lazy

from accounts.forms import UserSetPasswordForm


class UserPasswordResetView(PasswordResetView):
    template_name = "accounts/password/reset/reset.html"
    email_template_name = "accounts/password/reset/email/email.html"
    subject_template_name = "accounts/password/reset/email/subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password/reset/done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password/reset/confirm.html"
    form_class = UserSetPasswordForm
    success_url = reverse_lazy("accounts:password_reset_complete")


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password/reset/complete.html"
