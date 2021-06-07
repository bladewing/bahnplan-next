from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts import views as accounts_views
from . import views as accounts_views

urlpatterns = [
    url(r'^accounts/signup/$',
        accounts_views.signup,
        name='signup'),
    url(r'^accounts/logout/$',
        auth_views.LogoutView.as_view(),
        name='logout'),
    url(r'^accounts/login/$',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login'),
    url(r'^accounts/password_reset/$',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='password_reset'),
]