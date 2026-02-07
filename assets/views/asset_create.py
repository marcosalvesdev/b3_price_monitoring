from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from assets.forms import AssetCreateForm

from django.urls import reverse_lazy

from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError


class AssetCreateView(LoginRequiredMixin, CreateView):
    form_class = AssetCreateForm
    template_name = "assets/asset_create.html"
    success_url = reverse_lazy("assets:list")
    object = None

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                return self.form_valid(form)
            except IntegrityError as err:
                # TODO: Find a way to handle this error outside of the view,
                #  maybe in the model validation or in the form validation
                if "unique constraint" in str(err).lower():
                    err = ValidationError('An asset with this ticker already exists.')
                form.add_error(field=None, error=err)

                return self.form_invalid(form)
        else:
            return self.form_invalid(form)
