import datetime
#from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from core.models.criterion import Criterion
from core.models.leasing_mode import LeasingMode
from core.models.line import Line
from core.models.tender import Tender
from core.models.track import Track
from core.models.track_limit import TrackLimit
from core.models.vehicle import Vehicle
from core.models.vehicle_type import VehicleType


@login_required
def tenders_list_view(request):
    tenders = Tender.objects.filter(start_date__lte=datetime.datetime.now()).order_by('end_date')
    return render(request, 'tender_list.html', {'tenders': tenders})


def tenders_detail_view(request, pk):
    tender = get_object_or_404(Tender, pk=pk)
    platforms = TrackLimit.objects.filter(tender=tender).filter(time_to_reach_in_minutes=0)
    service_facilities = TrackLimit.objects.filter(tender=tender).filter(time_to_reach_in_minutes__gt=0)
    tracks = Track.objects.filter(tender=tender)
    lines = Line.objects.filter(tender=tender)
    criteria = Criterion.objects.filter(tender=tender)
    return render(request, 'tender_details.html', {
        'tender': tender,
        'service_facilities': service_facilities,
        'platforms': platforms,
        'lines': lines,
        'tracks': tracks,
        'criteria': criteria
    })


def vehicle_list_view(request):
    vehicles = Vehicle.objects.filter(owner=request.user.player.active_company)
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})


def vehicle_lease_view(request, pk):
    # TODO error when form input is not valid/no lease happened
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
