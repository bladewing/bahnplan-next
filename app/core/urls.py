from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('createcompany', views.create_company_view, name='createcompany'),
]
