from django.contrib import admin

# Register your models here.
from core.models.company import Company
from core.models.criterion import Criterion
from core.models.leasing_mode import LeasingMode
from core.models.line import Line
from core.models.route import Route
from core.models.station import Station
from core.models.tender import Tender
from core.models.track import Track
from core.models.track_limit import TrackLimit
from core.models.transport_requirement import TransportRequirement
from core.models.vehicle import Vehicle
from core.models.vehicle_type import VehicleType
from core.models.workshop_category import WorkshopCategory

admin.site.register(Vehicle)
admin.site.register(VehicleType)
admin.site.register(WorkshopCategory)
admin.site.register(Station)


class TrackInline(admin.TabularInline):
    model = Track


class TrackLimitInline(admin.TabularInline):
    model = TrackLimit


class LineInline(admin.TabularInline):
    model = Line


class WorkshopInline(admin.TabularInline):
    model = Tender.workshops.through


class CriterionInline(admin.TabularInline):
    model = Criterion


class TenderAdmin(admin.ModelAdmin):
    list_display = ('get_route_name', 'id', 'start_date', 'end_date', 'route', 'text')
    readonly_fields = ('id',)
    fields = ('id', 'start_date', 'end_date', 'route', 'text')
    inlines = [LineInline, TrackLimitInline, TrackInline, WorkshopInline, CriterionInline]

    def get_route_name(self, obj):
        return obj.route.name

    get_route_name.short_description = 'route'
    get_route_name.admin_order_field = 'route__name'


admin.site.register(Tender, TenderAdmin)


class TransportRequirementInline(admin.TabularInline):
    model = TransportRequirement


class LineAdmin(admin.ModelAdmin):
    inlines = [TransportRequirementInline]


admin.site.register(Line, LineAdmin)


class TrackAdmin(admin.ModelAdmin):
    model = Track


admin.site.register(Track, TrackAdmin)


class CompanyAdmin(admin.ModelAdmin):
    # fieldsets = [
    #    (None, {'fields': ['name']}),
    #    ('Date information', {'fields': ['date']})
    # ]
    list_display = ('name', 'abbrev', 'get_owners')

    @staticmethod
    def get_owners(obj):
        return "".join([u.username for u in obj.ownership.all()])


admin.site.register(Company, CompanyAdmin)


class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'operator', 'type', 'revenue_per_week', 'start_date', 'end_date')


admin.site.register(Route, RouteAdmin)


class LeasingModeAdmin(admin.ModelAdmin):
    list_display = ('name', 'factor_yearly', 'factor_weekly')


admin.site.register(LeasingMode, LeasingModeAdmin)
