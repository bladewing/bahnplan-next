from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CompanyCreationForm
from .models import Company


def index_view(request):
    """Main view"""
    return render(request, 'base.html')


@login_required()
def create_company_view(request):
    """
    Page where user can create a company
    """
    if request.method == "POST":
        form = CompanyCreationForm(request.POST)
        if form.is_valid():
            Company.create_owned_company(form.name, form.abbrev, request.user)
            return redirect('index')
    else:
        form = CompanyCreationForm
    return render(request, 'create_company.html', {'form': form})
