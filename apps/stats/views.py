from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg, Q
from django.db.models.functions import TruncMonth, TruncDay
from apps.transactions.models import Transaction
import datetime

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = datetime.date.today()
        month = int(request.query_params.get('month', today.month))
        year  = int(request.query_params.get('year',  today.year))

        qs = Transaction.objects.filter(user=request.user, date__month=month, date__year=year)
        totals = qs.aggregate(
            total_expenses=Sum('amount', filter=Q(type='expense')),
            total_income=Sum('amount',   filter=Q(type='income')),
        )
        total_expenses = float(totals['total_expenses'] or 0)
        total_income   = float(totals['total_income']   or 0)

        by_category = (
            qs.filter(type='expense')
            .values('category__id', 'category__name', 'category__color', 'category__icon')
            .annotate(total=Sum('amount'), count=Count('id'))
            .order_by('-total')
        )
        daily = (
            qs.annotate(day=TruncDay('date'))
            .values('day', 'type')
            .annotate(total=Sum('amount'))
            .order_by('day')
        )
        return Response({
            'period': {'month': month, 'year': year},
            'summary': {
                'total_expenses': total_expenses,
                'total_income': total_income,
                'balance': total_income - total_expenses,
            },
            'by_category': list(by_category),
            'daily_evolution': list(daily),
        })

class MonthlyEvolutionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = int(request.query_params.get('year', datetime.date.today().year))
        monthly = (
            Transaction.objects.filter(user=request.user, date__year=year)
            .annotate(month=TruncMonth('date'))
            .values('month', 'type')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )
        return Response({'year': year, 'monthly': list(monthly)})

class CategoryBreakdownView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today   = datetime.date.today()
        year    = int(request.query_params.get('year',  today.year))
        month   = request.query_params.get('month')
        tx_type = request.query_params.get('type', 'expense')

        qs = Transaction.objects.filter(user=request.user, date__year=year, type=tx_type)
        if month:
            qs = qs.filter(date__month=int(month))

        breakdown = (
            qs.values('category__id', 'category__name', 'category__color', 'category__icon')
            .annotate(total=Sum('amount'), count=Count('id'), average=Avg('amount'))
            .order_by('-total')
        )
        grand_total = sum(item['total'] for item in breakdown) or 1
        result = [dict(item, percent=round(float(item['total']) / float(grand_total) * 100, 1))
                  for item in breakdown]
        return Response({'type': tx_type, 'breakdown': result, 'grand_total': float(grand_total)})