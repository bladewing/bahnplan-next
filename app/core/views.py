import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from core.models.company import Company
from core.models.tender import Tender
from core.models.track_limit import TrackLimit
from core.models.track import Track
from core.models.line import Line
from core.models.criterion import Criterion

from .forms import CompanyCreationForm


def index_view(request):
    """Main view"""
    return render(request, 'base.html')


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