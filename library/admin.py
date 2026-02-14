from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'author', 'category', 'available_copies', 'total_copies', 'published_year')
    list_filter = ('category', 'published_year')
    search_fields = ('title_uz', 'title_ru', 'title_en', 'author', 'isbn')
    list_editable = ('available_copies',)
