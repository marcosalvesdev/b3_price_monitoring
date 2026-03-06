from accounts.views.login import UserLoginView as UserLoginView
from accounts.views.logout import UserLogoutView as UserLogoutView
from accounts.views.password_change import UserPasswordChangeDoneView as UserPasswordChangeDoneView
from accounts.views.password_change import UserPasswordChangeView as UserPasswordChangeView
from accounts.views.password_reset import (
    UserPasswordResetCompleteView as UserPasswordResetCompleteView,
)
from accounts.views.password_reset import (
    UserPasswordResetConfirmView as UserPasswordResetConfirmView,
)
from accounts.views.password_reset import UserPasswordResetDoneView as UserPasswordResetDoneView
from accounts.views.password_reset import UserPasswordResetView as UserPasswordResetView
from accounts.views.registration import UserRegistrationView as UserRegistrationView
