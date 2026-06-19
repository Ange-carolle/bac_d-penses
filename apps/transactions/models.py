from django.db import models
from django.conf import settings
from apps.categories.models import Category

class Transaction(models.Model):
    TYPE_EXPENSE = 'expense'
    TYPE_INCOME  = 'income'
    TYPE_CHOICES = [(TYPE_EXPENSE, 'Dépense'), (TYPE_INCOME, 'Revenu')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_EXPENSE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    note = models.TextField(blank=True)
    date = models.DateField()
    is_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.type} – {self.amount} ({self.date})"