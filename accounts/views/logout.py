from django.contrib.auth.views import LogoutView


class UserLogoutView(LogoutView):
    template_name = "accounts/logout.html"
    next_page = "accounts:login"
