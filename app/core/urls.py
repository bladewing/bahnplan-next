from django.urls import path

from core import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create_company', views.create_company_view, name='create-company'),
    path('tender_list', views.tenders_list_view, name='tender-list'),
    path('tender/<int:pk>', views.tenders_detail_view, name='tender-details'),
    path('company/transactions', views.TransactionView.as_view(), name='company_transactions'),
    path('vehicle_types_list', views.vehicle_types_list_view, name='vehicle-type-list'),
    path('vehicle_list', views.vehicle_list_view, name='vehicle-list'),
    path('vehicle_lease/<int:pk>', views.vehicle_lease_view, name='vehicle-lease'),
]
