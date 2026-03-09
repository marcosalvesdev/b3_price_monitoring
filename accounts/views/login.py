from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm
