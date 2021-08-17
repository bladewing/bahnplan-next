from django.views.generic import ListView

from core.models.vehicle import Vehicle
from core.views import IndexView
from core.views.breadcrumb_mixin import BreadcrumbMixin


class VehicleListView(BreadcrumbMixin, ListView):
    breadcrumb_url = 'vehicle-list'
    breadcrumb_name = 'Geleaste Fahrzeuge'
    parent = IndexView

    model = Vehicle
    template_name = 'vehicle_list.html'

    def get_queryset(self):
        return Vehicle.objects.filter(owner=self.request.user.player.active_company)
