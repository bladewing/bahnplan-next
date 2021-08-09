from datetime import timedelta

from django.utils import timezone
from django.views.generic import TemplateView

from core.models.company import Company
from core.models.route import Route
from core.models.tender import Tender
from core.models.vehicle import Vehicle
from core.models.workshop import Workshop
from core.utils.finance_utils import get_profit_for_week, account_balance
from core.views.breadcrumb_mixin import BreadcrumbMixin


class IndexView(BreadcrumbMixin, TemplateView):
    breadcrumb_url = 'index'
    breadcrumb_name = 'Startseite'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'number_of_companies': Company.objects.count(),
                'number_of_new_companies': Company.objects.filter(
                    creation_date__gte=timezone.now() - timedelta(days=14)).count(),
                'number_of_routes': Route.objects.count(),
                'number_of_routes_long_distance': Route.objects.filter(type=Route.LONG_DISTANCE).count(),
                'number_of_vehicles': Vehicle.objects.count(),
                'number_of_workshops': Workshop.objects.count(),
                'newest_tenders': self.newest_tenders(weeks=1),
                'next_starts': self.next_starts(weeks=2),
                'next_appointments': self.next_appointments(weeks=2),
                'profit_this_week': get_profit_for_week(self.get_active_company()),
                'profit_last_week': get_profit_for_week(self.get_active_company(), 1),
                'account_balance': account_balance(self.get_active_company()),
            }
        )
        return context

    @staticmethod
    def newest_tenders(weeks):
        fresh_tenders = Tender.objects.filter(start_date__gt=timezone.now() - timedelta(weeks=weeks))
        if fresh_tenders.count() >= 3:
            return fresh_tenders
        return Tender.objects.filter(end_date__gt=timezone.now()).order_by('-start_date')[:3]

    @staticmethod
    def next_appointments(weeks):
        return Tender.objects.filter(end_date__gt=timezone.now(), end_date__lte=timezone.now() + timedelta(
            weeks=weeks)).order_by('end_date')

    @staticmethod
    def next_starts(weeks):
        return Route.objects.filter(start_date__gt=timezone.now(), start_date__lt=timezone.now() + timedelta(
            weeks=weeks))
