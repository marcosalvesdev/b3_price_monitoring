from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

User = get_user_model()


class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
