from django.urls import path

from . import views
from .views import index_view

urlpatterns = [
    path('', index_view, name='index'),
]
