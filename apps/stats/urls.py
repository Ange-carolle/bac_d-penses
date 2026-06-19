from django.urls import path
from .views import DashboardView, MonthlyEvolutionView, CategoryBreakdownView

urlpatterns = [
    path('dashboard/',  DashboardView.as_view(),         name='stats-dashboard'),
    path('monthly/',    MonthlyEvolutionView.as_view(),  name='stats-monthly'),
    path('categories/', CategoryBreakdownView.as_view(), name='stats-categories'),
]
