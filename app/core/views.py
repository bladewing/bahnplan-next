import datetime
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView

from core.models.route import Route
from core.models.vehicle import Vehicle
from core.models.workshop import Workshop
from core.models.company import Company
from core.models.tender import Tender
from core.models.track_limit import TrackLimit
from core.models.track import Track
from core.models.line import Line
from core.models.criterion import Criterion
from core.models.leasing_mode import LeasingMode
from core.models.vehicle_type import VehicleType

from .forms import CompanyCreationForm



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
            Company.create_owned_company(form.data['name'], form.data['abbrev'], request.user)
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

def tenders_list_view(request):
    tenders = Tender.objects.filter(start_date__lte=datetime.datetime.now()).order_by('end_date')
    return render(request, 'tenders_list.html', {'tenders': tenders})


def tenders_detail_view(request, pk):
    tender = get_object_or_404(Tender, pk=pk)
    platforms = TrackLimit.objects.filter(tender=tender).filter(time_to_reach_in_minutes=0)
    servicefacilities = TrackLimit.objects.filter(tender=tender).filter(time_to_reach_in_minutes__gt=0)
    tracks = Track.objects.filter(tender=tender)
    lines = Line.objects.filter(tender=tender)
    criterions = Criterion.objects.filter(tender=tender)
    return render(request, 'tender_details.html', {
        'tender': tender,
        'servicefacilities': servicefacilities,
        'platforms': platforms,
        'lines': lines,
        'tracks': tracks,
        'criterions': criterions
    })


def vehicle_types_list_view(request):
    vehicle_types = VehicleType.objects.all()
    return render(request, 'vehicle_types_list.html', {'vehicle_types': vehicle_types})


def vehicle_list_view(request):
    vehicles = Vehicle.objects.filter(owner=request.user.player.activecompany)
    return render(request, 'vehicles_list.html', {'vehicles': vehicles})


def vehicle_lease_view(request, pk):
    # TODO error when form input is not valid/no lease happend
    if request.method == "POST":
        vehicle_type = VehicleType.objects.get(pk=request.POST.get("vehicleType"))
        amount = int(request.POST.get("amount"))
        leasing_mode = LeasingMode.objects.get(pk=request.POST.get("leasingMode"))
        if amount > 0 and leasing_mode is not None:
            Vehicle.create_vehicle(vehicle_type, leasing_mode, amount, request.user.player.activecompany)
            return redirect('vehicletypeslist')
    else:
        vehicle_type = VehicleType.objects.get(pk=pk)
        leasing_modes = LeasingMode.objects.all()
        return render(request, 'vehicle_lease.html', {'vehicle_type': vehicle_type, 'leasing_modes': leasing_modes})
