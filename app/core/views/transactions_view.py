from django.views.generic import ListView

from core.models.transaction import Transaction
from core.views import IndexView
from core.views.breadcrumb_mixin import BreadcrumbMixin


class TransactionView(BreadcrumbMixin, ListView):
    breadcrumb_url = 'company_transactions'
    breadcrumb_name = 'Buchungsübersicht'
    parent = IndexView
    model = Transaction
    template_name = 'company_transactions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'company': self.get_active_company()})
        return context

    def get_queryset(self):
        return Transaction.objects.filter(payer=self.get_active_company()) | Transaction.objects.filter(
            recipient=self.get_active_company())
