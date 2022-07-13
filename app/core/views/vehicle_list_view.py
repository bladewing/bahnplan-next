import datetime

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


class VehicleChangeLeaseView(BreadcrumbMixin, ListView):
    breadcrumb_url = 'vehicle-list'
    breadcrumb_name = 'Fahrzeug bearbeiten'
    parent = VehicleListView

    model = Vehicle
    template_name = 'vehicle_changelease.html'

    def get_queryset(self):
        selected_vehicles_as_text = self.request.POST.get("selected_vehicles")
        vehicles = Vehicle.objects.filter(owner=self.request.user.player.active_company).filter(
                pk__in=selected_vehicles_as_text_array)
        if self.request.method == "POST" and self.request.POST['submit'] == "change_lease":
            return vehicles
        if self.request.method == "POST" and self.request.POST['submit'] == "execute_changes":
            vehicles.update(leased_until=datetime.datetime.fromtimestamp(self.request.POST['new_leasing_end']))
