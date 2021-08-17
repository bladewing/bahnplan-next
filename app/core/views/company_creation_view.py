from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView

from core.forms import CompanyCreationForm
from core.models.company import Company
from core.views.breadcrumb_mixin import BreadcrumbMixin
from core.views.index_view import IndexView


class CreateCompanyView(BreadcrumbMixin, LoginRequiredMixin, FormView):
    breadcrumb_url = 'create-company'
    breadcrumb_name = 'Unternehmen erstellen'
    parent = IndexView

    template_name = 'create_company.html'
    form_class = CompanyCreationForm
    success_url = ''

    def form_valid(self, form):
        Company.create_owned_company(form.data['name'], form.data['abbrev'], self.request.user)
        return redirect('index')
