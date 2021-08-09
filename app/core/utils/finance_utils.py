from datetime import datetime, timedelta, date
from decimal import getcontext, Decimal

from django.db.models import Sum

from core.models.transaction import Transaction


def get_profit_between(company, start, end):
    income = Transaction.objects.filter(recipient=company,
                                        timestamp__gt=start,
                                        timestamp__lt=end).aggregate(Sum('amount'))
    spending = Transaction.objects.filter(payer=company,
                                          timestamp__gt=start,
                                          timestamp__lt=end).aggregate(Sum('amount'))
    getcontext().prec = 2
    return Decimal((income['amount__sum'] or 0) - (spending['amount__sum'] or 0))


def get_profit_for_week(company, offset=0):
    start_of_week = datetime.now() - timedelta(days=date.today().weekday(), weeks=offset)
    start_of_week = start_of_week.replace(minute=0, hour=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=7)
    return get_profit_between(company, start_of_week, end_of_week)


def account_balance(company):
    income = Transaction.objects.filter(recipient=company).aggregate(Sum('amount'))
    spending = Transaction.objects.filter(payer=company).aggregate(Sum('amount'))
    getcontext().prec = 2
    return Decimal((income['amount__sum'] or 0) - (spending['amount__sum'] or 0))
