# Register your models here.
from django.contrib import admin

<<<<<<< HEAD
# Register your models here.
from .models import Vehicle, VehicleType, WorkshopCategory, Company, Tender

admin.site.register(Vehicle)
admin.site.register(VehicleType)
admin.site.register(WorkshopCategory)
admin.site.register(Company)
admin.site.register(Tender)
=======
from core.models import Company, Route


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
    list_display = ('name', 'operator', 'type', 'revenue', 'start_date', 'end_date')


admin.site.register(Route)
>>>>>>> 933c05833a1daa8d2508d15f94ed9309f3141ea3
