from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import UserRegistrationForm

User = get_user_model()


class UserRegistrationView(CreateView):
    model = User
    template_name = "accounts/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("accounts:login")
