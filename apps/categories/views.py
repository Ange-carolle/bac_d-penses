from rest_framework import viewsets, filters
from django.db.models import Count
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']

    def get_queryset(self):
        qs = Category.objects.filter(user=self.request.user).annotate(
            transaction_count=Count('transactions')
        )
        is_income = self.request.query_params.get('is_income')
        if is_income is not None:
            qs = qs.filter(is_income=is_income.lower() == 'true')
        return qs