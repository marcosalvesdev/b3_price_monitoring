from django.urls import path

from accounts.views import (
    ProfileDeleteView,
    ProfileDetailView,
    ProfileUpdateView,
    UserLoginView,
    UserLogoutView,
    UserPasswordChangeDoneView,
    UserPasswordChangeView,
    UserPasswordResetCompleteView,
    UserPasswordResetConfirmView,
    UserPasswordResetDoneView,
    UserPasswordResetView,
    UserRegistrationView,
)

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("password_change/", UserPasswordChangeView.as_view(), name="password_change"),
    path(
        "password_change/done/", UserPasswordChangeDoneView.as_view(), name="password_change_done"
    ),
    path("password_reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "reset/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("reset/done/", UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("profile/", ProfileDetailView.as_view(), name="profile"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile_update"),
    path("profile/delete/", ProfileDeleteView.as_view(), name="profile_delete"),
]
