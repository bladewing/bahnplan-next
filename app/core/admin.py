from django.contrib import admin

# Register your models here.
from core.models.company import Company
from core.models.route import Route
from core.models.tender import Tender
from core.models.vehicle import Vehicle
from core.models.vehicle_type import VehicleType
from core.models.workshop_category import WorkshopCategory

admin.site.register(Vehicle)
admin.site.register(VehicleType)
admin.site.register(WorkshopCategory)
admin.site.register(Tender)


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
