# Register your models here.
from django.contrib import admin

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
