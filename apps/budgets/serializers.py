from rest_framework import serializers
from django.db.models import Sum
from apps.categories.serializers import CategorySerializer
from apps.transactions.models import Transaction
from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    spent     = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()
    percent   = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = ('id', 'category', 'category_detail', 'amount', 'period',
                  'month', 'year', 'spent', 'remaining', 'percent', 'created_at')
        read_only_fields = ('id', 'created_at')

    def _spent(self, obj):
        qs = Transaction.objects.filter(user=obj.user, category=obj.category, type='expense', date__year=obj.year)
        if obj.month:
            qs = qs.filter(date__month=obj.month)
        return float(qs.aggregate(s=Sum('amount'))['s'] or 0)

    def get_spent(self, obj):    return self._spent(obj)
    def get_remaining(self, obj): return float(obj.amount) - self._spent(obj)
    def get_percent(self, obj):
        return round(self._spent(obj) / float(obj.amount) * 100, 1) if float(obj.amount) else 0

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)