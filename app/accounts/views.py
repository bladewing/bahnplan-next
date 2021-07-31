from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse

from core.models.company import Company
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


class BreadcrumbsLoginView(LoginView):
    breadcrumb_name = 'Login'
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'breadcrumbs': [{'name': self.breadcrumb_name, 'link': reverse('login')}]})
        return context


def switch_company_view(request, pk):
    newcompany = Company.objects.get(pk=pk)
    if newcompany.ownership == request.user:
        request.user.player.active_company = newcompany
        request.user.player.save()
    else:
        print("WARNING: User " + request.user.username + " wants to switch to company " + newcompany.name +
              "which he doesn't own.")
    return redirect('index')  # TODO better redirect to the page where the user called the company switch
