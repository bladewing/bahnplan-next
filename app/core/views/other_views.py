import datetime
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from core.forms import CompanyCreationForm
from core.models.company import Company
from core.models.criterion import Criterion
from core.models.leasing_mode import LeasingMode
from core.models.line import Line
from core.models.tender import Tender
from core.models.track import Track
from core.models.track_limit import TrackLimit
from core.models.vehicle import Vehicle
from core.models.vehicle_type import VehicleType


def index_view(request):
    """Main view"""
    return render(request, 'index.html')


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


def tenders_list_view(request):
    tenders = Tender.objects.filter(start_date__lte=datetime.datetime.now()).order_by('end_date')
    return render(request, 'tender_list.html', {'tenders': tenders})


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
    vehicles = Vehicle.objects.filter(owner=request.user.player.active_company)
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})


def vehicle_lease_view(request, pk):
    # TODO error when form input is not valid/no lease happend
    if request.method == "POST":
        vehicle_type = VehicleType.objects.get(pk=request.POST.get("vehicleType"))
        amount = int(request.POST.get("amount"))
        leasing_mode = LeasingMode.objects.get(pk=request.POST.get("leasingMode"))
        if amount > 0 and leasing_mode is not None:
            Vehicle.create_vehicle(vehicle_type, leasing_mode, amount, request.user.player.active_company)
            return redirect('vehicle-type-list')
    else:
        vehicle_type = VehicleType.objects.get(pk=pk)
        leasing_modes = LeasingMode.objects.all()
        return render(request, 'vehicle_lease.html', {'vehicle_type': vehicle_type, 'leasing_modes': leasing_modes})
