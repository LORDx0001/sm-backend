from django.contrib import admin
from .models import KPIRecord

@admin.register(KPIRecord)
class KPIRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'score', 'created_at')
    list_filter = ('month', 'user__role')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    ordering = ('-month', 'user')
