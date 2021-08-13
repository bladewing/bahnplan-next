from django.views.generic import ListView

from core.models.vehicle_type import VehicleType
from core.views import IndexView
from core.views.breadcrumb_mixin import BreadcrumbMixin


class VehicleTypeView(BreadcrumbMixin, ListView):
    breadcrumb_url = 'vehicle-type-list'
    breadcrumb_name = 'Fahrzeugtypen'
    parent = IndexView
    model = VehicleType
    template_name = 'vehicle_types_list.html'
