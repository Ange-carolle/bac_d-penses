from django.db import models
from django.conf import settings
from apps.categories.models import Category

class Budget(models.Model):
    PERIOD_CHOICES = [('monthly', 'Mensuel'), ('yearly', 'Annuel')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly')
    month = models.PositiveSmallIntegerField(null=True, blank=True)
    year  = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', '-month']
        unique_together = ('user', 'category', 'month', 'year')

    def __str__(self):
        return f"Budget {self.category.name} – {self.amount}"