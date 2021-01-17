from django.contrib import admin

# Register your models here.
from core.models import Vehicle, VehicleType, WorkshopCategory, Company, Tender, Route

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

    def get_owners(self, obj):
        return "".join([u.username for u in obj.ownership.all()])

admin.site.register(Company, CompanyAdmin)

class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'operator', 'type', 'revenue_per_week', 'start_date', 'end_date')

admin.site.register(Route, RouteAdmin)
