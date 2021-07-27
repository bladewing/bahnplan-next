from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView

from .forms import CompanyCreationForm
from .models.company import Company
from .models.route import Route
from .models.tender import Tender
from .models.vehicle import Vehicle
from .models.workshop import Workshop


def index_view(request):
    """Main view"""
    return render(request, 'index.html')


class BreadcrumbTemplateView(TemplateView):
    breadcrumb_name = ""
    breadcrumb_url = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'breadcrumbs': [{'name': self.breadcrumb_name, 'link': reverse(self.breadcrumb_url)}]})
        return context


@login_required()
def create_company_view(request):
    """
    Page where user can create a company
    """
    if request.method == "POST":
        form = CompanyCreationForm(request.POST)
        if form.is_valid():
            Company.create_owned_company(form.name, form.abbrev, request.user)
            return redirect('index')
    else:
        form = CompanyCreationForm
    return render(request, 'create_company.html', {'form': form})


class IndexView(BreadcrumbTemplateView):
    breadcrumb_name = 'Startseite'
    breadcrumb_url = 'index'
    template_name = 'index.html'

    @staticmethod
    def newest_tenders():
        fresh_tenders = Tender.objects.filter(start_date__gt=timezone.now() - timedelta(days=7))
        if fresh_tenders.count() >= 3:
            return fresh_tenders
        return Tender.objects.filter(end_date__gt=timezone.now()).order_by('-start_date')[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'number_of_companies': Company.objects.count(),
                'number_of_new_companies': Company.objects.filter(
                    creation_date__gte=timezone.now() - timedelta(days=14)).count(),
                'number_of_routes': Route.objects.count(),
                'number_of_routes_long_distance': Route.objects.filter(type=Route.LONG_DISTANCE).count(),
                'number_of_vehicles': Vehicle.objects.count(),
                'number_of_workshops': Workshop.objects.count(),
                'newest_tenders': self.newest_tenders(),
                'next_starts': self.next_starts(),
                'next_appointments': self.next_appointments(),
                'profit_this_week': self.profit_this_week(),
                'profit_last_week': self.profit_last_week(),
                'account_balance': self.account_balance(),
            }
        )

        return context

    @staticmethod
    def next_starts():
        return Route.objects.filter(start_date__gt=timezone.now(), start_date__lt=timezone.now() + timedelta(weeks=2))

    @staticmethod
    def next_appointments():
        return Tender.objects.filter(end_date__gt=timezone.now(), end_date__lte=timezone.now() + timedelta(
            weeks=2)).order_by('end_date')

    @staticmethod
    def profit_this_week():
        return 0

    @staticmethod
    def profit_last_week():
        return 0

    @staticmethod
    def account_balance():
        return 0
