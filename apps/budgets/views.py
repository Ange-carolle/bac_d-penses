from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Budget
from .serializers import BudgetSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'period', 'month', 'year']

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).select_related('category')