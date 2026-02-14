from django.db import models
from django.conf import settings

class KPIRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='kpis')
    
    month = models.DateField() # e.g. 2026-02-01
    score = models.IntegerField(default=0) # 0-100
    
    comment = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'month']
        verbose_name = 'KPI Record'
        verbose_name_plural = 'KPI Records'

    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%Y-%m')} - {self.score}"
