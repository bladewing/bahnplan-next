from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CompanyCreationForm


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
            new_company = form.save(commit=False)
            new_company.save()
            new_company.ownership.add(request.user)
            new_company.save()
            return redirect('index')
    else:
        form = CompanyCreationForm
    return render(request, 'create_company.html', {'form': form})
