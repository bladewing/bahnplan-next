from django.urls import path

import core.views.vehicle_list_view
from core import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create_company', views.CreateCompanyView.as_view(), name='create-company'),
    path('tender_list', views.tenders_list_view, name='tender-list'),
    path('tender/<int:pk>', views.tenders_detail_view, name='tender-details'),
    path('tender/<int:pk>/apply', views.tenders_apply_view, name='tender-apply'),
    path('company/transactions', views.TransactionView.as_view(), name='company_transactions'),
    path('vehicle_types', views.VehicleTypeView.as_view(), name='vehicle-type-list'),
    path('vehicle_list', core.views.vehicle_list_view.VehicleListView.as_view(), name='vehicle-list'),
    path('vehicle_lease_change', core.views.vehicle_list_view.VehicleChangeLeaseView.as_view(), name='vehicle-change-lease'),
    path('vehicle_lease/<int:pk>', views.vehicle_lease_view, name='vehicle-lease'),
]
