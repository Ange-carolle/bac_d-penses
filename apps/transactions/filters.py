import django_filters
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    date_after  = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_before = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    amount_min  = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max  = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    month       = django_filters.NumberFilter(field_name='date', lookup_expr='month')
    year        = django_filters.NumberFilter(field_name='date', lookup_expr='year')

    class Meta:
        model = Transaction
        fields = ['type', 'category', 'is_recurring', 'date_after', 'date_before',
                  'amount_min', 'amount_max', 'month', 'year']