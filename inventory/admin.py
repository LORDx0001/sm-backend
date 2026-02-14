from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'category', 'quantity', 'unit', 'location', 'last_updated')
    list_filter = ('category', 'location')
    search_fields = ('name_uz', 'name_ru', 'name_en', 'description')
    list_editable = ('quantity', 'location')
