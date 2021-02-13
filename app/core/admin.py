from django.contrib import admin

# Register your models here.
from core.models import Vehicle, VehicleType, WorkshopCategory, Company, Tender, Route, Workshop, Station, TrackLimit, Criterion, TransportRequirement, Track, Line

admin.site.register(Vehicle)
admin.site.register(Workshop)
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
    list_display=('get_route_name', 'id' , 'start_date', 'end_date', 'route', 'text')
    readonly_fields=('id',)
    fields=('id', 'start_date', 'end_date', 'route', 'text')
    inlines=[TrackLimitInline, LineInline, WorkshopInline, CriterionInline]
    def get_route_name(self, obj):
        return obj.route.name
    get_route_name.short_description = 'route'
    get_route_name.admin_order_field = 'route__name'

admin.site.register(Tender, TenderAdmin)

class TransportRequirementInline(admin.TabularInline):
    model = TransportRequirement

class LineAdmin(admin.ModelAdmin):
    inlines=[TransportRequirementInline]

admin.site.register(Line, LineAdmin)

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
    list_display = ('name', 'operator', 'ttype', 'revenue_per_week', 'start_date', 'end_date')

admin.site.register(Route, RouteAdmin)
