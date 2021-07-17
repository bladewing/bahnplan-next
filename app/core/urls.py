from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('createcompany', views.create_company_view, name='createcompany'),
    path('tenderslist', views.tenders_list_view, name='tenderslist'),
    path('tender/<int:pk>', views.tenders_detail_view, name='tenderdetails'),
    path('vehicletypeslist', views.vehicle_types_list_view, name='vehicletypeslist'),
    path('vehicleslist', views.vehicle_list_view, name='vehicleslist'),
    path('vehicleslease/<int:pk>', views.vehicle_lease_view, name='vehiclelease'),
]
