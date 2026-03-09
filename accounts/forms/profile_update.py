from django import forms

from accounts.models import User


class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, "profile"):
            self.fields["avatar"].initial = self.instance.profile.avatar
