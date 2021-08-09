from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from core.models.company import Company
from core.views.breadcrumb_mixin import BreadcrumbMixin
from .forms import SignUpForm
from .models import Player


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.player = Player.objects.create(
                user=user)  # TODO untested. user should have a player object upon creation
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class BreadcrumbsLoginView(BreadcrumbMixin, LoginView):
    breadcrumb_url = 'login'
    breadcrumb_name = 'Login'
    template_name = "login.html"


def switch_company_view(request, pk):
    new_company = Company.objects.get(pk=pk)
    if new_company.ownership.filter(id=request.user.id).exists:
        request.user.player.active_company = new_company
        request.user.player.save()
    else:
        print("WARNING: User " + request.user.username + " wants to switch to company " + new_company.name +
              "which he doesn't own.")
    return redirect(
        request.META.get('HTTP_REFERER'))
