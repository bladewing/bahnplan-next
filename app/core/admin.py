from django.contrib import admin

# Register your models here.
from .models import Vehicle, VehicleType, WorkshopCategory, Company, Tender

admin.site.register(Vehicle)
admin.site.register(VehicleType)
admin.site.register(WorkshopCategory)
admin.site.register(Company)
admin.site.register(Tender)